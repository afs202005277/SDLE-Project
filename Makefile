.PHONY: databases

databases:
	@echo "Creating the 'databases' directory and subdirectories with files..."
	rm -rf databases
	mkdir -p databases/0 databases/1 databases/2
	touch databases/0/0.db databases/0/1.db databases/0/2.db
	touch databases/1/0.db databases/1/1.db databases/1/2.db
	touch databases/2/0.db databases/2/1.db databases/2/2.db
	@echo "Finished creating the 'databases' directory and subdirectories with files."

