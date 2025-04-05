//comment
package testFiles;

public class Test {//class comment

    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
    /**
     * This is a Javadoc comment
     * @since 1.0
     * @param args command line arguments
     * @deprecated This method is deprecated
     */ 

    public void testMethod() {
        // This is a test method
        System.out.println("This is a test method.");
    }

    public void anotherTestMethod() {
        /*
         This is another test method
        */
        System.out.println("This is //another test method.");
        System.out.println("This is /* another test method. */");
    }
}