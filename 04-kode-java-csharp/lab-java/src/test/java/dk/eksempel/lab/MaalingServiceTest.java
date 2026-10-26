package dk.eksempel.lab;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class MaalingServiceTest {

    private MaalingService service;

    @BeforeEach
    void setUp() {
        service = new MaalingService(new InMemMaalingRepository());
    }

    @Test
    void registrerGemmerMaalingMedNytId() {
        Maaling maaling = service.registrer(1, 21.3, 1013);

        assertEquals(1, maaling.id());
        assertEquals(21.3, maaling.temperatur());
    }

    @ParameterizedTest(name = "temperatur {0} og tryk {1} er gyldig")
    @CsvSource({
            "-50, 1000",
            "150, 1000",
            "20, 800",
            "20, 1100",
    })
    void graensevaerdierErGyldige(double temperatur, double tryk) {
        Maaling maaling = service.registrer(1, temperatur, tryk);

        assertEquals(temperatur, maaling.temperatur());
    }

    @ParameterizedTest(name = "temperatur {0} og tryk {1} afvises")
    @CsvSource({
            "-50.1, 1000",
            "150.1, 1000",
            "20, 799.9",
            "20, 1100.1",
    })
    void vaerdierUdenforIntervalletAfvises(double temperatur, double tryk) {
        assertThrows(UgyldigMaalingException.class, () -> service.registrer(1, temperatur, tryk));
    }

    @Test
    void gennemsnitBeregnesPrForsoeg() {
        service.registrer(1, 20, 1000);
        service.registrer(1, 30, 1000);
        service.registrer(2, 99, 1000);

        assertEquals(25.0, service.gennemsnitTemperatur(1).orElseThrow());
    }

    @Test
    void ingenGennemsnitForForsoegUdenMaalinger() {
        assertTrue(service.gennemsnitTemperatur(42).isEmpty());
    }

    @Test
    void varmeMaalingerFiltrererPaaGraense() {
        service.registrer(1, 20, 1000);
        service.registrer(1, 26, 1000);
        service.registrer(1, 29, 1000);

        assertEquals(2, service.varmeMaalinger(1, 25).size());
    }
}
