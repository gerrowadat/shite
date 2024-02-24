package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

var (
	clientSecretFile string
	authTokenFile    string

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
	rootCmd.PersistentFlags().StringVar(&clientSecretFile, "clientsecretfile", "sheets.key.json", "Client secret file")
	rootCmd.PersistentFlags().StringVar(&authTokenFile, "authtokenfile", "token.json", "where to store our oauth token")
}
