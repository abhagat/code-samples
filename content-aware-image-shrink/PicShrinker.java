package picShrink;
import java.awt.*;

/**
 * A collection of methods used in implementing Avidan and Shamir's content-
 * aware image resizing algorithm. The methods act on a PicGrabber object and
 * modify the image according to an energy function in the implementation.
 * 
 * @author abhagat
 * 
 */
public class PicShrinker {
    private PicGrabber picture;

    /** Constructor. Accepts PicGrabber object. */
    public PicShrinker(PicGrabber picture) {
        this.picture = picture;
    }

    /** Returns picture's width, in pixels. */
    public int width() {
        return picture.getWidth();
    }

    /** Returns picture's height, in pixels. */
    public int height() {
        return picture.getHeight();
    }
    
    /** Returns the picture */
    public PicGrabber getPicture() {
        return this.picture;
    }

    /**********************************************************
     * Methods for calculating pixel gradient *
     **********************************************************/
    private double gradientVal(int x, int y) {
        return xSquareGrad(x, y) + ySquareGrad(x, y);
    }

    private double xSquareGrad(int x, int y) {
        Color prev = picture.getPixelColor(x - 1, y);
        Color next = picture.getPixelColor(x + 1, y);
        return diffGradCalc(prev, next);
    }

    private double ySquareGrad(int x, int y) {
        Color prev = picture.getPixelColor(x, y - 1);
        Color next = picture.getPixelColor(x, y + 1);
        return diffGradCalc(prev, next);
    }

    private double diffGradCalc(Color prev, Color next) {
        double redGrad = next.getRed() - prev.getRed();
        double blueGrad = next.getBlue() - prev.getBlue();
        double greenGrad = next.getGreen() - prev.getGreen();
        return redGrad * redGrad + blueGrad * blueGrad + greenGrad * greenGrad;
    }

    /**
     * Return the calculated "energy" of a pixel at column x and column y.
     * Pixels at the edges of the image will contain the maximum energy,
     * 195075.0 as specified by the definition of the gradient function.
     * 
     * @param x
     * @param y
     * @return
     */
    private double energy(int x, int y) {
        if (x < 0 || x > picture.getWidth() - 1 || y < 0
                || y > picture.getHeight() - 1) {
            throw new IndexOutOfBoundsException(
                    "Program requested energy count for non-existent pixel.");
        } else if (x == 0 || x == picture.getWidth() - 1 || y == 0
                || y == picture.getHeight() - 1) {
            return 195075.0; // 3*255^2
        } else {
            // fancylanguage: this allows "level of abstraction" to experiment
            // with new energy functions
            return gradientVal(x, y);
        }
    }

    /**********************************************************
     * Methods for calculating energy seams *
     **********************************************************/
    // GENERAL IMPLEMENTATION NOTES
    //
    // seamList:
    // INVARIANT any entry in a seamList contains a double such that
    // going to the entry from the previous row (or column) represents lowest
    // possible energy required to reach that entry.
    //
    // energyArray:
    // Initialized with the values of each pixel's energy. After the algorithm
    // is run, energyArray MUST contain the energy required to reach pixel
    // (i, j) from the origin side of the picture.
    //
    // horizontal and vertical seam:
    // these functions act similarly - one will act on a transpose energy matrix
    // as compared to the other. therefore, modularizing the code to allow
    // for more readability and maintainability is important.
    //
    // horizontal and vertical should only initialize the proper variables
    // they should both call the same functions to do the actual work

    /**
     * Returns a sequence of indices where a lowest-energy vertical seam is
     * present.
     * 
     * @return
     */
    // initializing vertSeamList is not necessary -- TODO
    protected int[] verticalSeam() {
        int w = picture.getWidth();
        int h = picture.getHeight();
        int[][] vertSeamList = new int[w][h];
        double[][] energyArray = new double[w][h];

        // initialize energy array
        for (int i = 0; i < w; i++) {
            for (int j = 0; j < h; j++) {
                energyArray[i][j] = energy(i, j);
            }
        }
        return calculateSeam(energyArray, vertSeamList);
    }

    /**
     * Returns a sequence of indices where a lowest-energy horizontal seam is
     * present.
     * 
     * @return
     */
    // initializing horSeamList is not necessary --TODO
    protected int[] horizontalSeam() {
        int h = picture.getWidth(); // transpose -- all else remains equal as
        // compared with vertSeam
        int w = picture.getHeight(); // transpose -- all else remains equal
        int[][] horSeamList = new int[w][h];
        double[][] energyArray = new double[w][h];

        // initialize energy array (transposed) -- tentative, index testing
        // needed
        for (int i = 0; i < w; i++) {
            for (int j = 0; j < h; j++) {
                energyArray[i][j] = energy(j, i);
            }
        }
        return calculateSeam(energyArray, horSeamList);
    }

    private void computeMinPathEnergies(double[][] energyArray, int[][] seamList) {
        int h = energyArray.length;
        int w = energyArray[0].length;
        // compute shortest paths to any pixel
        for (int j = 1; j < w - 1; j++) {
            for (int i = 0; i < h; i++) {
                // check the prior row - from where is the shortest path?
                int selected = 0;
                if (i == 0) { // checking left side of the picture, only two
                    // adjacent pixels above it
                    double optTwo = energyArray[i][j - 1];
                    double optThree = energyArray[i + 1][j + 1];
                    if (optThree < optTwo) {
                        selected = i + 1;
                    } else {
                        selected = i;
                    }
                } else if (i == w - 1) { // checking right side of the picture
                    double optOne = energyArray[i - 1][j - 1];
                    double optTwo = energyArray[i][j - 1];

                    if (optOne < optTwo) {
                        selected = i - 1;
                    } else {
                        selected = i;
                    }
                } else {
                    double optOne = energyArray[i - 1][j - 1];
                    double optTwo = energyArray[i][j - 1];
                    double optThree = energyArray[i + 1][j - 1];

                    if (optThree < optTwo && optOne < optThree) {
                        selected = i + 1;
                    } else if (optOne < optTwo && optOne < optThree) {
                        selected = i - 1;
                    } else {
                        selected = i;
                    }
                }

                // selected goes into seamList for this (i, j)
                seamList[i][j] = selected;
                
                energyArray[i][j] = energyArray[selected][j - 1]
                        + energyArray[i][j];
            }
        }
    }

    private int getMinIndex(double[][] e) {
        int h = e.length;
        int w = e[0].length;
        // search through all pixels at the bottom to find min-energy path end
        int min_index = 0;
        for (int i = 0; i < w; i++) {
            if (e[i][h - 1] < e[min_index][h - 1]) {
                min_index = i;
            }
        }
        return min_index;
    }

    /**
     * Return a "trace" of all pixels traversed as part of the minimum-energy
     * seam.
     */
    private int[] getTrace(int min_index, int[][] seamList) {
        int h = seamList.length;
        // having the min energy path end, trace back up the picture to find the
        // array
        int[] trace = new int[h];
        trace[h - 1] = min_index;
        int next_index = seamList[min_index][h - 1];
        for (int j = h - 1; j > 0; j--) {
            trace[j - 1] = next_index;
            if (j == 1)
                break;
            next_index = seamList[next_index][j - 1];
        }
        return trace;
    }

    private int[] calculateSeam(double[][] energyArray, int[][] seamList) {
        computeMinPathEnergies(energyArray, seamList);
        int min_index = getMinIndex(energyArray);
        return getTrace(min_index, seamList);
    }

    /**********************************************************
     * Methods for removing a seam from the picture *
     **********************************************************/
    // GENERAL IMPLEMENTATION NOTES
    // As it does not seem possible for BufferedImage to remove and shift
    // pixels,
    // a new PicGrabber will need to be instantiated.
    // Means a significant overhead for each removed seam.
    // It may be possible to combine/modularize these functions, but due to
    // reversed
    // indices, it may be impractical.

    /**
     * Remove a pre-calculated vertical seam from the picture. The pixel
     * locations of the "seam" are given as the input array.
     * 
     * @param a
     */
    public void removeVertSeam(int[] a) {
        int newWidth = width() - 1;
        int newHeight = height();

        PicGrabber newpic = new PicGrabber(newWidth, newHeight);
        int omitPixel; // in each row, a pixel not copied over to the new image
        boolean flag = false; // detects whether the omitted pixel has been
        // passed

        for (int j = 0; j < height(); j++) {
            omitPixel = a[j];
            for (int i = 0; i < width(); i++) {
                if (i == omitPixel) {
                    flag = true;
                    continue;
                } else if (flag == true) {
                    newpic.setPixelColor(i - 1, j, picture.getPixelColor(i, j));
                } else {
                    newpic.setPixelColor(i, j, picture.getPixelColor(i, j));
                }
            }
            flag = false;
        }
        picture = newpic;
    }

    /**
     * Remove a pre-calculated horizontal seam from the picture. The pixel
     * locations of the "seam" are given as the input array.
     * 
     * @param a
     */
    public void removeHorSeam(int[] a) {
        int newWidth = width();
        int newHeight = height() - 1;
        PicGrabber newpic = new PicGrabber(newWidth, newHeight);
        int omitPixel;
        boolean flag = false;

        for (int j = 0; j < width(); j++) {
            omitPixel = a[j];
            for (int i = 0; i < height(); i++) {
                if (i == omitPixel) {
                    flag = true;
                    continue;
                } else if (flag == true) {
                    newpic.setPixelColor(j, i-1, picture.getPixelColor(i, j));
                } else {
                    newpic.setPixelColor(j, i, picture.getPixelColor(i, j));
                }
            }
            flag = false;
        }
        picture = newpic;
    }

}
