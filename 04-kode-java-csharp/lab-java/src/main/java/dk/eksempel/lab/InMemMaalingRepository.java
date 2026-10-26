package dk.eksempel.lab;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Gemmer målinger i hukommelsen. Bruges i tests og i Main. */
public class InMemMaalingRepository implements MaalingRepository {

    private final Map<Long, Maaling> maalinger = new HashMap<>();

    @Override
    public Maaling gem(Maaling maaling) {
        maalinger.put(maaling.id(), maaling);
        return maaling;
    }

    @Override
    public List<Maaling> findForForsoeg(long forsoegId) {
        List<Maaling> resultat = new ArrayList<>();
        for (Maaling m : maalinger.values()) {
            if (m.forsoegId() == forsoegId) {
                resultat.add(m);
            }
        }
        return resultat;
    }

    @Override
    public long naesteId() {
        return maalinger.size() + 1;
    }
}
