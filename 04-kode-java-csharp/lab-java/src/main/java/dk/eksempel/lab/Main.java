package dk.eksempel.lab;

public class Main {

    public static void main(String[] args) {
        MaalingService service = new MaalingService(new InMemMaalingRepository());

        service.registrer(1, 20.1, 1013.2);
        service.registrer(1, 23.7, 1008.8);
        service.registrer(1, 28.9, 1008.3);

        System.out.println("Gennemsnit: " + service.gennemsnitTemperatur(1).orElseThrow());
        System.out.println("Over 25 °C: " + service.varmeMaalinger(1, 25));

        try {
            service.registrer(1, 999, 1013);
        } catch (UgyldigMaalingException e) {
            System.out.println("Afvist: " + e.getMessage());
        }
    }
}
