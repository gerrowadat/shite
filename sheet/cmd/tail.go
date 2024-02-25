package cmd

import (
	"context"
	"errors"
	"fmt"
	"log"
	"strconv"

	"github.com/gerrowadat/shite/sheet/gsheets"
	"github.com/spf13/cobra"
	"google.golang.org/api/option"
	"google.golang.org/api/sheets/v4"
)

// tailCmd represents the tail command
var (
	tailCmd = &cobra.Command{
		Args: func(cmd *cobra.Command, args []string) error {
			// Need exactly 2 args (sheet ID and data range)
			if err := cobra.ExactArgs(3)(cmd, args); err != nil {
				return err
			}
			// Validate whther arg 3 is a number
			if _, err := strconv.Atoi(args[2]); err != nil {
				return errors.New("argument 3 must be a number")

			}
			return nil
		},
		Use:   "tail <spreadsheet ID> <worksheet name> <number of rows>",
		Short: "Show the last few lines of a worksheet",
		Long: `Show the last few non-blank lines in a worksheet.
	e.g.:
	# Show the last 10 lines of the 'myworksheet' worksheet. 
	> sheet tail SpReAdShEetId myworksheet 10`,
		Run: func(cmd *cobra.Command, args []string) {
			doTail(cmd, args)
		},
	}
)

func init() {
	rootCmd.AddCommand(tailCmd)
}

func doTail(cmd *cobra.Command, args []string) {
	ctx := context.Background()
	client := gsheets.GetClient(clientSecretFile, authTokenFile)

	srv, err := sheets.NewService(ctx, option.WithHTTPClient(client))
	if err != nil {
		log.Fatalf("Unable to retrieve Sheets client: %v", err)
	}

	resp, err := srv.Spreadsheets.Get(args[0]).Do()
	if err != nil {
		log.Fatalf("Unable to retrieve sheet Id %v: %v", args[0], err)
	}

	if len(resp.Sheets) == 0 {
		log.Fatalf("Sheet ID %v has no sheets", args[0])
	}

	for _, sheet := range resp.Sheets {
		if sheet.Properties.Title == args[1] {
			// Properties.GridProperties.RowCount gives the grid size, not the amunt of data.
			// This seems to be 1000 for new sheets, so expensively poll through it.
			last_datarow := findLastDataRow(srv, args, sheet.Properties.GridProperties.RowCount)
			tail_lines, err := strconv.Atoi(args[2])
			if err != nil {
				log.Fatal("argument 3 must be a number")
			}
			// We get the last line by default
			tail_lines--
			dataspec := fmt.Sprintf("%v!%v:%v", args[1], max(1, last_datarow-int64(tail_lines)), last_datarow)
			log.Printf("tail: requesting %v->%v\n", args[0], dataspec)
			resp, err := srv.Spreadsheets.Values.Get(args[0], dataspec).Do()
			if err != nil {
				log.Fatalf("Unable to retrieve data from sheet at %v: %v", dataspec, err)
			}
			gsheets.PrintValues(resp)
			return
		}
	}
	// If we get here, we didn't find our worksheet.
	log.Fatalf("unable to find worksheet %v in spreadsheet %v", args[1], args[0])
}

func findLastDataRow(srv *sheets.Service, args []string, chunk_end int64) int64 {
	if chunk_end == 1 {
		return 0
	}

	chunk_start := max(1, chunk_end-int64(chunkSize))

	// worksheet!chunk_start:chunk_end
	dataspec := fmt.Sprintf("%v!%v:%v", args[1], chunk_start, chunk_end)

	resp, err := srv.Spreadsheets.Values.Get(args[0], dataspec).Do()
	if err != nil {
		log.Fatalf("Unable to retrieve data from sheet: %v", err)
	}

	// We get no values back if there is no data, so the first non-zero length chunk we see
	// scanning backwards from eof is the end of our data.
	if len(resp.Values) > 0 {
		return chunk_start + int64(len(resp.Values)-1)
	} else {
		return findLastDataRow(srv, args, chunk_start)
	}
}
