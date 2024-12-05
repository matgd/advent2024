package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

const FILENAME = "input.txt"

type intSet map[int]struct{}
type intIntSetMap map[int]intSet

func (s intSet) add(i int) {
	if _, ok := s[i]; !ok {
		s[i] = struct{}{}
	}
}

func (s intIntSetMap) add(k, v int) {
	if _, ok := s[k]; !ok {
		s[k] = intSet{}
	}
	s[k].add(v)
}

func (s intIntSetMap) contains(k, v int) bool {
	if _, ok := s[k]; !ok {
		return false
	}
	_, ok := s[k][v]
	return ok
}

func (s intIntSetMap) containsAny(k int, v []int) bool {
	for _, val := range v {
		if s.contains(k, val) {
			return true
		}
	}
	return false
}

func main() {
	input, _ := ioutil.ReadFile(FILENAME)
	inputLines := strings.Split(string(input), "\n")
	rules := intIntSetMap{}
	pageUpdates := make([][]int, 0, 100)
	for _, line := range inputLines {
		if strings.Contains(line, "|") {
			split := strings.Split(line, "|")
			page, _ := strconv.Atoi(split[0])
			pageRule, _ := strconv.Atoi(split[1])
			rules.add(page, pageRule)
		} else if strings.Contains(line, ",") {
			split := strings.Split(line, ",")
			currentPageUpdates := make([]int, 0, len(split))
			for _, s := range split {
				page, _ := strconv.Atoi(s)
				currentPageUpdates = append(currentPageUpdates, page)
			}
			pageUpdates = append(pageUpdates, currentPageUpdates)
		}
	}
	part1(rules, pageUpdates)
}

func part1(rules intIntSetMap, pageUpdates [][]int) {
	validIndexes := make([]int, 0, 100)
	for i, pageUpdate := range pageUpdates {
		validOrder := true
		for j := range pageUpdate {
			if rules.containsAny(pageUpdate[j], pageUpdate[:j]) {
				validOrder = false
				break
			}
		}
		if validOrder {
			validIndexes = append(validIndexes, i)
		}
	}

	sum := 0
	for _, vi := range validIndexes {
		sum += pageUpdates[vi][len(pageUpdates[vi])/2]
	}
	fmt.Println("Part 1:", sum) // 5452
}
