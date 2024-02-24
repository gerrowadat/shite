package gsheets

import (
	"fmt"

	"google.golang.org/api/sheets/v4"
)

func PrintValues(v *sheets.ValueRange) {
	for _, row := range v.Values {
		for i := range row {
			fmt.Print(row[i])
			if i != len(row)-1 {
				fmt.Print(",")
			}
		}
		fmt.Print("\n")
	}

}
