package cmd

import (
	"context"
	"errors"
	"fmt"
	"log"

	"github.com/gerrowadat/shite/sheet/gsheets"
	"github.com/spf13/cobra"
	"google.golang.org/api/option"
	"google.golang.org/api/sheets/v4"
)

// Implement an enum-a-like for the output-format flag
type OutputFormatValue interface {
	String() string
	Set(string) error
	Type() string
}

type OutputFormat string

const (
	csvFormat OutputFormat = "csv"
	tsvFormat OutputFormat = "tsv"
)

func (f *OutputFormat) String() string { return string(*f) }
func (f *OutputFormat) Type() string   { return "OutputFormat" }
func (f *OutputFormat) Set(v string) error {
	switch v {
	case "csv", "tsv":
		*f = OutputFormat(v)
		return nil
	default:
		return errors.New("invalid OutputFormat. Allowed [csv|tsv]")
	}
}

// getCmd represents the get command
var (
	outputFormat = csvFormat
	getCmd       = &cobra.Command{
		Args: func(cmd *cobra.Command, args []string) error {
			// Need exactly 2 args (sheet ID and data range)
			if err := cobra.ExactArgs(2)(cmd, args); err != nil {
				return err
			}
			// Validate data range spec.
			if !gsheets.IsValidDataSpec(args[1]) {
				return fmt.Errorf("invalid data spec: %v", args[1])
			}
			return nil
		},
		Use:   "get <spreadsheet-id> <datarange>",
		Short: "get a rang of data from a sheet",
		Long: `Get data given a spreadsheet ID and a range specifier.
	For example:
	  > sheet get SprEaDsHeeTiD 'rawdata!A3:G5'
`,
		Run: func(cmd *cobra.Command, args []string) {
			doGet(cmd, args)
		},
	}
)

func init() {
	rootCmd.AddCommand(getCmd)

	getCmd.PersistentFlags().Var(&outputFormat, "output-format", "Output format ([csv|tsv])")

}

func doGet(cmd *cobra.Command, args []string) {
	ctx := context.Background()
	client := gsheets.GetClient(clientSecretFile, authTokenFile)

	srv, err := sheets.NewService(ctx, option.WithHTTPClient(client))
	if err != nil {
		log.Fatalf("Unable to retrieve Sheets client: %v", err)
	}

	resp, err := srv.Spreadsheets.Values.Get(args[0], args[1]).Do()
	if err != nil {
		log.Fatalf("Unable to retrieve data from sheet: %v", err)
	}

	if len(resp.Values) == 0 {
		fmt.Println("No data found.")
	} else {
		for _, row := range resp.Values {
			for i, val := range row {
				fmt.Printf("%v", val)
				if i < len(row)-1 {
					fmt.Printf(",")
				} else {
					fmt.Println()
				}
			}
		}
	}
}
