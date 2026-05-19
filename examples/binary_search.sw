scene recursive_search(arr, target, left, right) {
  nodona (left > right) {
    packup -1
  }

  idhu mid = (left + right) // 2

  nodona (arr[mid] == target) {
    packup mid
  } illandre (arr[mid] < target) {
    packup recursive_search(arr, target, mid + 1, right)
  } climax {
    packup recursive_search(arr, target, left, mid - 1)
  }
}

scene binary_search(arr, target) {
  idhu start_left = 0
  idhu start_right = size(arr) - 1
  packup recursive_search(arr, target, start_left, start_right)
}

scene main() {
  idhu prime_movies = [1, 3, 5, 7, 9, 11]
  idhu target_hit = 7
  idhu position = binary_search(prime_movies, target_hit)
  dialogue(position)
}