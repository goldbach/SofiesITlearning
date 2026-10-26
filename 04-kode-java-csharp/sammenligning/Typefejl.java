import java.util.List;

public class Typefejl {
    static double gennemsnit(List<Double> maalinger) {
        double sum = 0;
        for (double m : maalinger) {
            sum += m;
        }
        return sum / maalinger.size();
    }

    public static void main(String[] args) {
        System.out.println("Starter beregning ...");
        System.out.println(gennemsnit(List.of(20.1, 21.3, 22.0)));
        System.out.println(gennemsnit("21.3"));
        System.out.println("Færdig");
    }
}
