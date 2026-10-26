package dk.eksempel.lab;

/**
 * En enkelt måling i et forsøg. Et record er en uforanderlig dataklasse:
 * Java genererer selv constructor, getters, equals og toString.
 */
public record Maaling(long id, long forsoegId, double temperatur, double tryk) {
}
