import java.io.BufferedReader;
import java.io.FileReader;
import java.io.PrintWriter;
import java.util.StringTokenizer;

public class LenFilter {
	public static void main(String[] args) throws Throwable {
		if (args.length != 8) {
			System.err
					.println("Usage: LenFilter in.fr in.en out.fr out.en maxWordsFr maxWordsEn maxWordLenFr maxWordLenEn");
			System.exit(1);
		}

		BufferedReader inFr = new BufferedReader(new FileReader(args[0]));
		BufferedReader inEn = new BufferedReader(new FileReader(args[1]));
		PrintWriter outFr = new PrintWriter(args[2]);
		PrintWriter outEn = new PrintWriter(args[3]);
		int maxWordsFr = Integer.parseInt(args[4]);
		int maxWordsEn = Integer.parseInt(args[5]);
		int maxWordLenFr = Integer.parseInt(args[6]);
		int maxWordLenEn = Integer.parseInt(args[7]);

		String line_fr;
		String line_en;
		while ((line_fr = inFr.readLine()) != null) {
			line_en = inEn.readLine();
			StringTokenizer tok_fr = new StringTokenizer(line_fr);
			StringTokenizer tok_en = new StringTokenizer(line_en);
            // No blank lines
            if (tok_fr.countTokens() == 0
                    || tok_en.countTokens() == 0)
                continue;
			if (tok_fr.countTokens() > maxWordsFr
					|| tok_en.countTokens() > maxWordsEn)
				continue;
			boolean bad = false;
			while (tok_fr.hasMoreTokens())
				if (tok_fr.nextToken().length() > maxWordLenFr) {
					bad = true;
					break;
				}
			if (bad)
				continue;
			while (tok_en.hasMoreTokens())
				if (tok_en.nextToken().length() > maxWordLenEn) {
					bad = true;
					break;
				}
			if (bad)
				continue;
			outFr.println(line_fr);
			outEn.println(line_en);
		}

		outFr.close();
		outEn.close();
	}
}
