import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.StringTokenizer;

public class KBestNgrams {

	static class NgramCount {
		public Hashtable<ArrayList<Integer>, double[]> count = new Hashtable<ArrayList<Integer>, double[]>();
		private Hashtable<String, Integer> map = new Hashtable<String, Integer>();
		private Hashtable<Integer, String> unmap = new Hashtable<Integer, String>();
		private int next = 1;

		public int map(String s) {
			Integer i = map.get(s);
			if (i == null) {
				i = next++;
				map.put(s, i);
				unmap.put(i, s);
			}
			return i;
		}

		public String unmap(int i) {
			return unmap.get(i);
		}
	}

	public static void main(String[] args) throws Throwable {
		if (args.length != 2) {
			System.err
					.println("Usage: KBestNgrams metric order < kbest.scored > ngrams.out");
			System.exit(1);
		}

		String metric = args[0] + "="; // bleu=100, find 100
		int order = Integer.parseInt(args[1]);

		NgramCount ngramCount = new NgramCount();

		BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		String line;

		int lc = 0;
		while ((line = in.readLine()) != null) {
			lc += 1;
			if (lc % 100000 == 0)
				System.err.println(lc);
			int j = line.indexOf("||");
			int k = line.indexOf("||", j + 3);
			String hyp = line.substring(j + 3, k);
			for (int i = 0; i < 3; i++, k = line.indexOf("||", k + 3))
				;
			k = line.indexOf(metric, k + 3);
			int l = line.indexOf(' ', k + metric.length() + 1);
			// Might be last entry in line
			double score = Double
					.parseDouble(l > -1 ? line.substring(k + metric.length(), l)
							: line.substring(k + metric.length()));
			// System.out.println(score + " " + hyp);
			ngrams(hyp, score, ngramCount, order);
		}
		Enumeration<ArrayList<Integer>> e = ngramCount.count.keys();
		while (e.hasMoreElements()) {
			ArrayList<Integer> ngram = e.nextElement();
			double[] sums = ngramCount.count.get(ngram);
			System.out.println(ngramString(ngram, ngramCount) + "\t" + sums[0]
					/ sums[1]);
		}
	}

	// Get ngrams from a line, add to count table
	private static void ngrams(String s, double score, NgramCount ngramCount,
			int order) {

		StringTokenizer tok = new StringTokenizer(s);
		int[] words = new int[tok.countTokens()];
		for (int i = 0; tok.hasMoreTokens(); words[i++] = ngramCount.map(tok
				.nextToken()))
			;

		for (int i = 0; i < words.length; i++) {
			ArrayList<Integer> ngram = new ArrayList<Integer>(order);
			for (int j = 0; j < order; j++) {
				if (i + j > words.length - 1)
					continue;
				ngram.add(words[i + j]);
				double[] entry = ngramCount.count.get(ngram);
				if (entry == null) {
					entry = new double[2];
					ngramCount.count.put(new ArrayList<Integer>(ngram), entry);
				}
				entry[0] += score;
				entry[1]++;
			}
		}
	}

	private static String ngramString(ArrayList<Integer> ngram,
			NgramCount ngramCount) {
		StringBuilder sb = new StringBuilder();
		for (int i : ngram) {
			sb.append(ngramCount.unmap(i));
			sb.append(" ");
		}
		return sb.toString().trim();
	}
}
