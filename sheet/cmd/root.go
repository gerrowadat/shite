package cmd

import (
	"errors"
	"os"

	"github.com/spf13/cobra"
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

var (
	outputFormat     = csvFormat
	clientSecretFile string
	authTokenFile    string
	chunkSize        int

	rootCmd = &cobra.Command{
		Use:   "sheet",
		Short: "Manipulate google sheet data",
		Long: `A utility to send and recieve data to/from a google
sheet from the command line in various forms.`,
		// Uncomment the following line if your bare application
		// has an action associated with it:
		// Run: func(cmd *cobra.Command, args []string) { },
	}
)

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().StringVar(&clientSecretFile, "clientsecretfile", "", "Client secret file")
	rootCmd.PersistentFlags().StringVar(&authTokenFile, "authtokenfile", "", "where to store our oauth token")

	rootCmd.PersistentFlags().IntVar(&chunkSize, "read-chunksize", 100, "How many rows at a time to read while fetching data")
	rootCmd.PersistentFlags().Var(&outputFormat, "output-format", "Output format ([csv|tsv])")
}
