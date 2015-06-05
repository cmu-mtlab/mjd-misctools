import java.io.BufferedReader;
import java.io.FileReader;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.Scanner;

public class Thresh {
	public static void main(String[] args) throws Throwable {
		if (args.length < 6) {
			System.err
					.println("usage: Thresh src.in tgt.in feats.in src.out tgt.out val1 [val2 ...]");
			System.exit(1);
		}

		BufferedReader inSrc = new BufferedReader(new FileReader(args[0]));
		BufferedReader inTgt = new BufferedReader(new FileReader(args[1]));
		BufferedReader inFeats = new BufferedReader(new FileReader(args[2]));
		PrintWriter outSrc = new PrintWriter(args[3]);
		PrintWriter outTgt = new PrintWriter(args[4]);

		float[] thresh = new float[args.length - 5];
		for (int i = 0; i < args.length - 5; i++)
			thresh[i] = Float.parseFloat(args[i + 5]);

		System.err.println(Arrays.toString(thresh));
		String feats;
		int lc = 0;
		int kept = 0;
		while ((feats = inFeats.readLine()) != null) {
			lc += 1;
			if (lc % 100000 == 0)
				System.err.println(lc + "(" + kept + ")");
			String src = inSrc.readLine();
			String tgt = inTgt.readLine();
			Scanner sc = new Scanner(feats);
			boolean good = true;
			for (float t : thresh) {
				float s = sc.nextFloat();
				if (s < t) {
					good = false;
					break;
				}
			}
			if (good) {
				kept += 1;
				outSrc.println(src);
				outTgt.println(tgt);
			}

		}

        outSrc.close();
        outTgt.close();
        System.err.println(lc + "(" + kept + ")");
	}
}
