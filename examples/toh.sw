scene hanoi(n, source_rod, destination_rod, helper_rod) {
  nodona (n == 1) {
    dialogue("Move disk 1 from " + source_rod + " to " + destination_rod)
    packup 1
  }
  
  // Step 1: Move top n-1 disks from source to helper
  hanoi(n - 1, source_rod, helper_rod, destination_rod)
  
  // Step 2: Move the nth disk from source to destination
  dialogue("Move disk " + n + " from " + source_rod + " to " + destination_rod)
  
  // Step 3: Move the n-1 disks from helper to destination
  hanoi(n - 1, helper_rod, destination_rod, source_rod)
}

scene main() {
  idhu total_disks = 3
  dialogue("--- Sandalwood Action Dynamic Testing Begin ---")
  hanoi(total_disks, "Rod-A", "Rod-C", "Rod-B")
  dialogue("--- Climax Super Hit, Mission Packed Up! ---")
}