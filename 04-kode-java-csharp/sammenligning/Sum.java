public class Sum {
    public static void main(String[] args) {
        long start = System.nanoTime();
        long total = 0;
        for (long i = 0; i < 100_000_000L; i++) {
            total += i % 7;
        }
        System.out.printf("%d %.2f s%n", total, (System.nanoTime() - start) / 1e9);
    }
}
