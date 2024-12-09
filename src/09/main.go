package main

import (
	"fmt"
	"os"
)

const FREE_SPACE int16 = -1

func main() {
	filename := os.Args[1]
	input, _ := os.ReadFile(filename)
	input_u8 := make([]uint8, len(input))
	for i, v := range input {
		input_u8[i] = v - '0' // unicode magic
	}
	part1(input_u8)
}

func getDiskSpace(input []uint8) (diskSpace []*int16, idLocalization map[int16][]int) {
	diskSpace = make([]*int16, 0, (len(input)+1)*9)
	idLocalization = map[int16][]int{}
	for i, v := range input {
		for spaceIndex := uint8(0); spaceIndex < v; spaceIndex++ {
			var value *int16
			if i%2 == 0 {
				value = new(int16)
				*value = int16(i / 2)
			} else {
				value = new(int16)
				*value = FREE_SPACE
			}
			diskSpace = append(diskSpace, value)
			if _, ok := idLocalization[*value]; !ok {
				idLocalization[*value] = []int{}
			}
			idLocalization[*value] = append(idLocalization[*value], len(diskSpace)-1)
		}
	}
	return
}

func printDiskSpace(diskSpace []*int16) {
	for _, space := range diskSpace {
		if *space == FREE_SPACE {
			fmt.Print(".")
		} else {
			fmt.Print(*space)
		}
	}
	fmt.Println()
}

func isEverythingMoved(diskSpace []*int16) bool {
	metFree := false
	for _, space := range diskSpace {
		if *space == FREE_SPACE {
			metFree = true
		}
		if *space != FREE_SPACE {
			if metFree {
				return false
			}
		}
	}
	return true
}

func move(input []uint8) (diskSpace []*int16, idLocalization map[int16][]int) {
	diskSpace, idLocalization = getDiskSpace(input)
	lastFileId := int16(len(input) / 2)
	for i := lastFileId; i >= 0; i-- {
		loc := idLocalization[i]
		for j := len(loc) - 1; j >= 0; j-- {
			firstFreeIndex := idLocalization[FREE_SPACE][0]
			filePartToMove := loc[j]
			*diskSpace[firstFreeIndex] ^= *diskSpace[filePartToMove]
			*diskSpace[filePartToMove] ^= *diskSpace[firstFreeIndex]
			*diskSpace[firstFreeIndex] ^= *diskSpace[filePartToMove]
			idLocalization[FREE_SPACE] = idLocalization[FREE_SPACE][1:]
			idLocalization[FREE_SPACE] = append(idLocalization[FREE_SPACE], filePartToMove)
			idLocalization[i] = idLocalization[i][:len(idLocalization[i])-1]
			if isEverythingMoved(diskSpace) {
				return
			}
		}
	}
	return
}

func moveWholeFiles(input []uint8) (diskSpace []*int16, idLocalization map[int16][]int) {
	diskSpace, idLocalization = getDiskSpace(input)
	lastFileId := int16(len(input) / 2)
	for i := lastFileId; i >= 0; i-- {
		loc := idLocalization[i]
		for j := len(loc) - 1; j >= 0; j-- {
			firstFreeIndex := idLocalization[FREE_SPACE][0]
			filePartToMove := loc[j]
			*diskSpace[firstFreeIndex] ^= *diskSpace[filePartToMove]
			*diskSpace[filePartToMove] ^= *diskSpace[firstFreeIndex]
			*diskSpace[firstFreeIndex] ^= *diskSpace[filePartToMove]
			idLocalization[FREE_SPACE] = idLocalization[FREE_SPACE][1:]
			idLocalization[FREE_SPACE] = append(idLocalization[FREE_SPACE], filePartToMove)
			idLocalization[i] = idLocalization[i][:len(idLocalization[i])-1]
			if isEverythingMoved(diskSpace) {
				return
			}
		}
	}
	return
}

func part1(input []uint8) {
	diskSpace, _ := move(input)
	checksum := 0
	for i, space := range diskSpace {
		if *space == FREE_SPACE {
			break
		}
		checksum += int(*space) * i
	}
	fmt.Println("Part 1:", checksum) // 6337921897505
}

func part2(input []uint8) {
}
