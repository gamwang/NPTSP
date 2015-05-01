import java.io.*;
import java.util.*;
class Test {
    public static void main (String[] args) throws IOException {
        int T = 1; // number of test cases
        PrintWriter fout = new PrintWriter (new FileWriter (new File ("answer.out")));
        for (int t = 1; t <= T; t++) {
            Scanner fin = new Scanner (new File (t + ".in"));
            int N = fin.nextInt();
            int[][] d = new int[N][N];
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    d[i][j] = fin.nextInt();
                }
            }
            char[] c = fin.next().toCharArray();

            // find an answer here, and put into assign
            int[] assign = new int[N];
            for (int i = 0; i < N; i++) {
                assign[i] = i+1;
            }

            fout.print(assign[0]);
            for (int i = 1; i < N; i++)
                fout.print (" " + assign[i]);
           fout.println();
        }
       fout.close();
    }
}
