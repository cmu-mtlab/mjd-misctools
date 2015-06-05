import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.StringTokenizer;

/**
 * This is a simple example of extracting a column from a CSV file by index or
 * name. For now, we're assuming that our files use a simple non-quoted
 * tab-delimited format (\t is the escape code for tab in Java):
 * 
 * field1\tfield2\tfield3
 * 
 * For quoted CSV files that look like this:
 * 
 * "field1","field2","field3"
 * 
 * there are many available Java CSV parsers such as
 * http://opencsv.sourceforge.net/
 * 
 */
public class CSVExtractor {

	// Why do we need to say main throws IOException (FileNotFoundException)?
	public static void main(String[] args) throws IOException {

		/*
		 * Help message if run with no arguments or unsupported number of
		 * arguments:
		 * 
		 * CSVExtractor
		 */

		if (args.length == 0 || args.length == 2 || args.length > 3) {
			System.err
					.println("Extract a column from a CSV file by index or name");
			// Why do we need to escape certain characters in Strings? Why would
			// we quote a column name when calling this program?
			System.err
					.println("usage: CSVExtractor <csvFile> [-i colIdx | -n \"colName\"]");
			System.exit(2);
		}

		/*
		 * Open our file
		 */

		String csvFile = args[0];
		// What is a BufferedReader? For now we just need to know this opens a
		// file to be read sequentially.
		BufferedReader csvIn = new BufferedReader(new FileReader(csvFile));

		/*
		 * Get our list of column names
		 */

		// Why are we reading a line? (We're treating this as a plain text file)
		String firstLine = csvIn.readLine();
		// What is an ArrayList? Why do we need to say this is a list of
		// Strings? Why not just use an array (String[])?
		ArrayList<String> colNames = new ArrayList<String>();
		// What is a StringTokenizer?
		StringTokenizer tok = new StringTokenizer(firstLine, "\t");
		// How is this loop working? What is it testing for and when does it
		// exit?
		while (tok.hasMoreTokens()) {
			// Why can we nest method calls like this? Is it good form to nest
			// too many method calls?
			colNames.add(tok.nextToken());
		}
		// What is a Hashtable? Why do we want to keep a dictionary of field
		// names instead of just a list?
		Hashtable<String, Integer> nameToIdx = new Hashtable<String, Integer>();
		// What is this loop doing? What does ++ mean?
		for (int i = 0; i < colNames.size(); i++) {
			nameToIdx.put(colNames.get(i), i);
		}

		/*
		 * One arg: only print column names:
		 * 
		 * CSVExtractor csvFile
		 */

		if (args.length == 1) {
			// What is this loop doing? Why would we use this instead of an
			// indexed loop? Could we also use an indexed loop here?
			for (String name : colNames) {
				// What's going on with String formatting here?
				String formatted = String.format("%d: %s", nameToIdx.get(name),
						name);
				System.out.println(formatted);
			}
			System.exit(0);
		}

		/*
		 * Three args: extract by index or name
		 */

		int idx = -1;
		// Why do we need to use equals instead of == for Strings?
		if (args[1].equals("-i")) {
			// Why do we need to use parseInt?
			idx = Integer.parseInt(args[2]);
			// What is this checking? Hint: it's in the error message.
			if (idx < 0 || idx >= colNames.size()) {
				System.err.println(String.format(
						"Error: column out of range \"%d\"", idx));
				System.exit(1);
			}
		} else if (args[1].equals("-n")) {
			// What is this checking?
			if (!nameToIdx.containsKey(args[2])) {
				System.err.println(String.format(
						"Error: no such column name \"%s\"", args[2]));
				System.exit(1);
			}
			// Why don't we need to convert anything here (no parseInt)?
			idx = nameToIdx.get(args[2]);
		} else {
			System.err.println("Syntax error: use -i or -n");
			System.exit(1);
		}

		// Reading a file line by line: what's going on here? What is being
		// assigned and what is being tested?
		String line;
		while ((line = csvIn.readLine()) != null) {
			// Why don't we need to declare an array in advance or give it a
			// length?
			String[] fields = line.split("\t");
			System.out.println(fields[idx]);
		}
	}
}
