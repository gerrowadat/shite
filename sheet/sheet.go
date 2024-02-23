package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"os"

	"golang.org/x/oauth2/google"
	"google.golang.org/api/option"
	"google.golang.org/api/sheets/v4"
)

var authfile = flag.String("clientsecretfile", "sheets.key.json", "Path to the JSON client secret file")
var tokfile = flag.String("authtokenfile", "token.json", "Path to the saved oauth token file")
var sheetid = flag.String("sheetid", "", "GSheets Spreadsheet ID")
var datarange = flag.String("datarange", "", "GSheets range to read")

func main() {
	flag.Parse()
	ctx := context.Background()

	if sheetid == nil || *sheetid == "" {
		log.Fatalf("Sheet ID is required")
	}

	if datarange == nil || *datarange == "" {
		log.Fatalf("Data range is required")
	}

	b, err := os.ReadFile(*authfile)
	if err != nil {
		log.Fatalf("Unable to read client secret file: %v", err)
	}

	// If modifying these scopes, delete your previously saved token.json.
	config, err := google.ConfigFromJSON(b, "https://www.googleapis.com/auth/spreadsheets.readonly")
	if err != nil {
		log.Fatalf("Unable to parse client secret file to config: %v", err)
	}
	client := getClient(config, *tokfile)

	srv, err := sheets.NewService(ctx, option.WithHTTPClient(client))
	if err != nil {
		log.Fatalf("Unable to retrieve Sheets client: %v", err)
	}

	resp, err := srv.Spreadsheets.Values.Get(*sheetid, *datarange).Do()
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
