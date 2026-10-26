package dk.eksempel.lab;

import java.util.List;
import java.util.OptionalDouble;

/**
 * Forretningsreglerne for målinger.
 *
 * <p>Regler aftalt med laboratoriet:
 * <ul>
 *   <li>Temperatur skal ligge mellem -50 og 150 °C, begge grænser inklusive.</li>
 *   <li>Tryk skal ligge mellem 800 og 1100 hPa, begge grænser inklusive.</li>
 * </ul>
 */
public class MaalingService {

    static final double MIN_TEMPERATUR = -50;
    static final double MAX_TEMPERATUR = 150;
    static final double MIN_TRYK = 800;
    static final double MAX_TRYK = 1100;

    private final MaalingRepository repository;

    public MaalingService(MaalingRepository repository) {
        this.repository = repository;
    }

    public Maaling registrer(long forsoegId, double temperatur, double tryk) {
        if (temperatur < MIN_TEMPERATUR || temperatur > MAX_TEMPERATUR) {
            throw new UgyldigMaalingException("Temperatur uden for gyldigt interval: " + temperatur);
        }
        if (tryk < MIN_TRYK || tryk >= MAX_TRYK) {
            throw new UgyldigMaalingException("Tryk uden for gyldigt interval: " + tryk);
        }
        Maaling maaling = new Maaling(repository.naesteId(), forsoegId, temperatur, tryk);
        return repository.gem(maaling);
    }

    public OptionalDouble gennemsnitTemperatur(long forsoegId) {
        return repository.findForForsoeg(forsoegId).stream()
                .mapToDouble(Maaling::temperatur)
                .average();
    }

    public List<Maaling> varmeMaalinger(long forsoegId, double graense) {
        return repository.findForForsoeg(forsoegId).stream()
                .filter(m -> m.temperatur() > graense)
                .toList();
    }
}
