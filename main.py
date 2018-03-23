import apriori

def main():
	algo = apriori.Apriori('../sample_datasets/config.csv')
	algo.RunApriori()


if __name__ == "__main__":
	main()
