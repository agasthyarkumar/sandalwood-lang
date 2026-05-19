scene find_gcd(a, b) {
  nodona (b == 0) {
    packup a
  }
  packup find_gcd(b, a % b)
}

scene main() {
  idhu num1 = 56
  idhu num2 = 98
  idhu result = find_gcd(num1, num2)
  
  dialogue("--- GCD Box Office Tracking ---")
  dialogue("GCD of 56 and 98 is:")
  dialogue(result) 
}