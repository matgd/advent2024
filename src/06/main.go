package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

const FILENAME = "input.txt"

type Direction string

const (
	UP    Direction = "-y"
	DOWN  Direction = "+y"
	LEFT  Direction = "-x"
	RIGHT Direction = "+x"
)

type mapSquare struct {
	timesVisited int
	isObstacle   bool
	guardHere    bool
}

type mapManager struct {
	squares       [][]mapSquare
	guardLocation [2]int
	guardFacing   Direction
}

func (mm mapManager) print() {
	for y, row := range mm.squares {
		for x, square := range row {
			if mm.guardLocation[0] == y && mm.guardLocation[1] == x {
				switch mm.guardFacing {
				case UP:
					fmt.Print("^")
				case DOWN:
					fmt.Print("v")
				case LEFT:
					fmt.Print("<")
				case RIGHT:
					fmt.Print(">")
				}
			} else if square.isObstacle {
				fmt.Print("#")
			} else {
				toPrint := "."
				if square.timesVisited > 0 {
					toPrint = strconv.Itoa(square.timesVisited)
				}
				fmt.Print(toPrint)
			}
		}
		fmt.Println()
	}
}

func (mm mapManager) squaresVisited() int {
	visited := 0
	for _, row := range mm.squares {
		for _, square := range row {
			if square.timesVisited > 0 {
				visited++
			}
		}
	}
	return visited
}

func (mm *mapManager) moveGuard(y, x int) {
	mm.squares[mm.guardLocation[0]][mm.guardLocation[1]].guardHere = false
	mm.squares[y][x].guardHere = true
	mm.squares[y][x].timesVisited++
	mm.guardLocation = [2]int{y, x}
}

// Returns:
// - whether there is an obstacle in front of the guard
// - the y coordinates of the square in front of the guard
// - the x coordinates of the square in front of the guard
// - is the guard facing out of bounds
func (mm mapManager) obstacleInFrontOfGuard() (bool, int, int, bool) {
	gy, gx := mm.guardLocation[0], mm.guardLocation[1]
	var gyFront, gxFront int
	switch mm.guardFacing {
	case UP:
		gyFront, gxFront = gy-1, gx
	case DOWN:
		gyFront, gxFront = gy+1, gx
	case LEFT:
		gyFront, gxFront = gy, gx-1
	case RIGHT:
		gyFront, gxFront = gy, gx+1
	default:
		panic("invalid direction")
	}
	if gyFront < 0 || gxFront < 0 || gyFront >= len(mm.squares) || gxFront >= len(mm.squares[0]) {
		return false, gyFront, gxFront, true
	}
	return mm.squares[gyFront][gxFront].isObstacle, gyFront, gxFront, false
}

func (mm *mapManager) turnGuardRight() {
	switch mm.guardFacing {
	case UP:
		mm.guardFacing = RIGHT
	case RIGHT:
		mm.guardFacing = DOWN
	case DOWN:
		mm.guardFacing = LEFT
	case LEFT:
		mm.guardFacing = UP
	}
}

func (mm *mapManager) oneGuardTurn() bool {
	obs, newY, newX, oob := mm.obstacleInFrontOfGuard()
	for obs {
		mm.turnGuardRight()
		obs, newY, newX, oob = mm.obstacleInFrontOfGuard()
	}
	if oob {
		return false
	}
	mm.moveGuard(newY, newX)
	return true
}

func main() {
	input, _ := os.ReadFile(FILENAME)
	manager := mapManager{[][]mapSquare{}, [2]int{-1, -1}, UP}

	for y, line := range strings.Split(string(input), "\n") {
		if len(line) == 0 {
			continue
		}
		squareRow := []mapSquare{}
		for x, square := range line {
			switch square {
			case '#':
				squareRow = append(squareRow, mapSquare{0, true, false})
			case '^': // starts with facing up in input
				squareRow = append(squareRow, mapSquare{1, false, true})
				manager.guardLocation = [2]int{y, x}
			default:
				squareRow = append(squareRow, mapSquare{0, false, false})
			}
		}
		manager.squares = append(manager.squares, squareRow)
	}

	part1(manager)
}

func part1(mm mapManager) {
	for mm.oneGuardTurn() {
	}
	fmt.Println(mm.squaresVisited())
}
