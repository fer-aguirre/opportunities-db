# Import modules
import opportunities_db.data.load as load
import opportunities_db.data.analyze as analyze
import opportunities_db.data.export as export
import logging
import os


def main():

    # Load data
    data_processed = load.data_processed
    new_version = load.new_version
    sqlite = load.sqlite

    # Read data
    df1 = analyze.read_csv(data_processed)
    df2 = analyze.read_csv(new_version)

    # Process data
    diff = analyze.compare_data(df1, df2)

    # If there's new data
    if len(diff) != 0:
        # Create empty lists
        texts = []
        titles = []
        deadlines = []
        summaries = []
        try:
            # Iterate over the list of urls
            for i in range(len(diff)):

                # Make HTTP request
                soup = analyze.make_request(diff[i])

                # Extract the text
                text = analyze.extract_text(soup)
                texts.append(text)

                # Extract the title
                title = analyze.extract_title(soup)
                titles.append(title)

                # Extract the deadline
                deadline = analyze.extract_deadline(diff[i])
                deadlines.append(deadline)

                # Extact a summary
                summary = analyze.extract_summary(diff[i])
                summaries.append(summary)

            # Create a dataframe from lists
            df_new = analyze.create_dataframe(titles, deadlines, summaries, diff)
            export.update_data(df1, df_new)

            # Convert csv file to sqlite
            os.system(f"csvs-to-sqlite {data_processed} {sqlite}")

            # Update log file
            logging.basicConfig(filename="log.txt", level=logging.INFO,
                                format="%(asctime)s %(message)s")
            logging.info("Database updated")
            
        except Exception:
            logging.basicConfig(filename="log.txt", level=logging.ERROR,
                    format="%(asctime)s %(message)s")
            logging.exception("Exception info")


if __name__ == '__main__':
    main()
