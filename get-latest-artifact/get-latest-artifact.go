package main

import (
	"context"
	"flag"
	"fmt"
	"github.com/google/go-github/v56/github"
	"log"
	"time"
)

func main() {
	repoOwner := flag.String("repo-owner", "andvarienterprises", "repo owner or org")
	repoName := flag.String("repo-name", "www.strategichopes.co", "repo name")
	outputInfo := flag.String("output", "archiveurl", "output [name|url|archiveurl]")
	flag.Parse()

	client := github.NewClient(nil)
	ctx := context.Background()
	artifacts, _, err := client.Actions.ListArtifacts(ctx, *repoOwner, *repoName, nil)
	if err != nil {
		fmt.Printf("Error: %s", err)
		return
	}

	log.Printf("Found %d artifacts.", *artifacts.TotalCount)
	if *artifacts.TotalCount == 0 {
		return
	}

	// Set 'newest' to unix epoch, then find the actual newest.
	newest := github.Artifact{CreatedAt: &github.Timestamp{time.Unix(0, 0)}}
	for _, a := range artifacts.Artifacts {
		log.Printf(" - Artifact %s created at %s\n", *a.Name, *a.CreatedAt)
		if a.CreatedAt.GetTime().After(*newest.CreatedAt.GetTime()) {
			newest = *a
		}
	}

	log.Printf("%s is the newest artifact.\n", *newest.Name)

	switch *outputInfo {
	case "name":
		fmt.Println(*newest.Name)
	case "url":
		fmt.Println(*newest.URL)
	case "archiveurl":
		fmt.Println(*newest.ArchiveDownloadURL)
	default:
		log.Fatal("Must specify name, url or archiveurl to --output")
	}

}
