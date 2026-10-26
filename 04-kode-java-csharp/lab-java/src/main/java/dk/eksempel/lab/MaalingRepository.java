package dk.eksempel.lab;

import java.util.List;

/**
 * Kontrakten for, hvordan målinger gemmes og hentes. Servicen kender kun
 * dette interface, ikke om data ligger i hukommelsen eller i en database.
 */
public interface MaalingRepository {

    Maaling gem(Maaling maaling);

    List<Maaling> findForForsoeg(long forsoegId);

    long naesteId();
}
