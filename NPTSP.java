import java.io.*;
import java.util.Scanner;
import java.util.ArrayList;
class NPTSP {
    public static void main(String args[] ) throws Exception {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT */
        Scanner sc = new Scanner(System.in);
        int len = Integer.parseInt(sc.nextLine());
        int[][] adjMat = new int[len][];
        for (int i = 0; i < len; i += 1) {
          String row = sc.nextLine();
          String[] tmp = row.split(" ");
          adjMat[i] = new int[len];
          for (int j = 0; j < len; j += 1) {
            adjMat[i][j] = Integer.parseInt(tmp[0]);
          }
        }
        String[] colorMat = sc.nextLine().split(" ");
        solve(adjMat, colorMat);    
    }
    
    static void solve(int[][] adjMat, String[] colorMat) {
      // Solve the TSP and print it out to STDOUT
    }
}
