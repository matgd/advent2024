package main

import (
	"fmt"
	"os"
	"strings"
)

func buildGreatWall(width int) []uint8 {
	greatWall := make([]uint8, width, width)
	for i := 0; i < width; i++ {
		greatWall[i] = 99
	}
	return greatWall
}

func main() {
	filename := os.Args[1]
	input, _ := os.ReadFile(filename)
	splitInput := strings.Split(string(input), "\n")
	topology := [][]uint8{}
	trailheadLocations := [][2]uint8{}
	topology = append(topology, buildGreatWall(len(splitInput)+1))
	for y, line := range splitInput {
		yRow := []uint8{}
		yRow = append(yRow, 99)
		for x, xChar := range line {
			if xChar == '.' {
				yRow = append(yRow, 77)
				continue
			}
			val := uint8(xChar - '0')
			yRow = append(yRow, val)
			if val == 0 {
				trailheadLocations = append(trailheadLocations, [2]uint8{uint8(y + 1), uint8(x + 1)})
			}
		}
		yRow = append(yRow, 99)
		topology = append(topology, yRow)
	}
	topology = append(topology, buildGreatWall(len(splitInput)+1))
	fmt.Printf("topology: %v\n", topology)

	solution(topology, trailheadLocations)
}

func canReach9(topology [][]uint8, currentLocation [2]uint8, currentHeight uint8, ogLocation [2]uint8) int {
	currY, currX := currentLocation[0], currentLocation[1]
	for true {
		if topology[currY][currX] == 9 {
			fmt.Println("grep this sorted unique toilet", ogLocation, currY, currX)
			return 1
		}
		topDiff := topology[currY-1][currX] - currentHeight
		leftDiff := topology[currY][currX-1] - currentHeight
		rightDiff := topology[currY][currX+1] - currentHeight
		bottomDiff := topology[currY+1][currX] - currentHeight
		diffs := [4]uint8{topDiff, leftDiff, rightDiff, bottomDiff}
		ones := [4]uint8{0, 0, 0, 0}
		onesSum := 0
		for i, diff := range diffs {
			if diff == 1 {
				ones[i] = 1
				onesSum++
			}
		}

		if onesSum > 1 {
			topFound, leftFound, rightFound, bottomFound := 0, 0, 0, 0
			if topDiff == 1 {
				topFound = canReach9(topology, [2]uint8{currY - 1, currX}, currentHeight+1, ogLocation)
			}
			if leftDiff == 1 {
				leftFound = canReach9(topology, [2]uint8{currY, currX - 1}, currentHeight+1, ogLocation)
			}
			if rightDiff == 1 {
				rightFound = canReach9(topology, [2]uint8{currY, currX + 1}, currentHeight+1, ogLocation)
			}
			if bottomDiff == 1 {
				bottomFound = canReach9(topology, [2]uint8{currY + 1, currX}, currentHeight+1, ogLocation)
			}
			return topFound + leftFound + rightFound + bottomFound
		} else if onesSum == 1 {
			if topDiff == 1 {
				currY = currY - 1
			} else if leftDiff == 1 {
				currX = currX - 1
			} else if rightDiff == 1 {
				currX = currX + 1
			} else if bottomDiff == 1 {
				currY = currY + 1
			}
			currentHeight++
		} else {
			return 0
		}
	}
	return 0
}

func solution(topology [][]uint8, trailheadLocations [][2]uint8) {
	hikingTrails := 0
	for _, yx := range trailheadLocations {
		hikingTrails += canReach9(topology, yx, 0, yx)
	}
	fmt.Printf("hikingTrails: %v\n", hikingTrails)
	// part 1: go run main.go input.txt | grep this | sort | uniq | wc -l
}
