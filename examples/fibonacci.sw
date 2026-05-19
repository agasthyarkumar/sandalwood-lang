scene fibonacci(n) {
  nodona (n <= 1) {
    packup n
  }
  packup fibonacci(n - 1) + fibonacci(n - 2)
}

scene main(){dialogue(fibonacci(2))}