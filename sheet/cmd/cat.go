/*
Copyright © 2024 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"context"
	"fmt"
	"log"

	"github.com/gerrowadat/shite/sheet/gsheets"
	"github.com/spf13/cobra"
	"google.golang.org/api/option"
	"google.golang.org/api/sheets/v4"
)

// catCmd represents the cat command
var catCmd = &cobra.Command{
	Use:   "cat <spreadsheet ID> <worksheet name>",
	Short: "Output the contents of a worksheet",
	Run: func(cmd *cobra.Command, args []string) {
		doCat(cmd, args)
	},
}

func init() {
	rootCmd.AddCommand(catCmd)
}

func doCat(cmd *cobra.Command, args []string) {
	ctx := context.Background()
	client := gsheets.GetClient(clientSecretFile, authTokenFile)

	srv, err := sheets.NewService(ctx, option.WithHTTPClient(client))
	if err != nil {
		log.Fatalf("Unable to retrieve Sheets client: %v", err)
	}

	start := 1
	// --read-chunksize
	end := chunkSize
	dataspec := fmt.Sprintf("%v!%v:%v", args[1], start, end)

	resp, err := srv.Spreadsheets.Values.Get(args[0], dataspec).Do()
	if err != nil {
		log.Fatalf("Unable to retrieve data from sheet: %v", err)
	}

	for {
		gsheets.PrintValues(resp)

		if len(resp.Values) < chunkSize {
			break
		}

		start = 1 + end
		end = start + (chunkSize - 1)
		dataspec = fmt.Sprintf("%v!%v:%v", args[1], start, end)
		fmt.Println(dataspec)
		resp, err = srv.Spreadsheets.Values.Get(args[0], dataspec).Do()
		if err != nil {
			log.Fatalf("Unable to retrieve data from sheet: %v", err)
		}
	}
}
