package dk.eksempel.lab;

public class UgyldigMaalingException extends RuntimeException {

    public UgyldigMaalingException(String besked) {
        super(besked);
    }
}
