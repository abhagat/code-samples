package picShrink;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;
import picShrink.PicShrinker;
import picShrink.PicGrabber;
import java.awt.Color;


public class PicShrinkerTest {
    
    @Test
    public void testCorrectHorizontalSeamCalculationTop() {
        PicGrabber p = basicTestPicture();
        PicShrinker ps = new PicShrinker(p);
        int[] a = ps.horizontalSeam();
        assertEquals(4, a.length);
        assertEquals(0, a[2]);
        assertEquals(0, a[3]);
    }
    
    @Test
    public void testCorrectHorizontalSeamCalculationBottom() {
        PicGrabber p = basicTestPictureInverted();
        PicShrinker ps = new PicShrinker(p);
        int[] a = ps.horizontalSeam();
        assertEquals(4, a.length);
        assertEquals(1, a[0]);
        assertEquals(1, a[1]);
    }
    
    @Test
    public void testCorrectVerticalSeamCalculationLeft() {
        PicGrabber p = basicTestPicture();
        PicShrinker ps = new PicShrinker(p);
        int[] a = ps.verticalSeam();
        assertEquals(4, a.length);
        assertEquals(1, a[0]);
        assertEquals(1, a[1]);
    }
    
    @Test
    public void testCorrectVerticalSeamCalculationRight() {
        PicGrabber p = basicTestPictureInverted();
        PicShrinker ps = new PicShrinker(p);
        int[] a = ps.verticalSeam();
        assertEquals(4, a.length);
        assertEquals(1, a[0]);
        assertEquals(1, a[1]);
    }
    
    @Test
    public void testCorrectHorizontalRowRemoved() {
        PicGrabber p = basicTestPicture();
        PicShrinker ps = new PicShrinker(p);
        ps.removeHorSeam(ps.horizontalSeam());
        p = ps.getPicture();
        assertEquals(Color.YELLOW, p.getPixelColor(2, 1));
    }
    
    @Test
    public void testCorrectVerticalRowRemoved() {   
        PicGrabber p = basicTestPicture();
        PicShrinker ps = new PicShrinker(p);
        ps.removeVertSeam(ps.verticalSeam());
        p = ps.getPicture();
        assertEquals(Color.YELLOW, p.getPixelColor(1, 2));    
    }
    
    /**
     * Sets up a 4x4 picture whose pixels are:
     * (BLACK) (BLACK) (BLACK) (BLACK)
     * (BLACK) (RED) (RED) (BLACK)
     * (BLACK) (RED) (YELLOW) (BLACK)
     * (BLACK) (BLACK) (BLACK) (BLACK)
     * 
     * In this case, a row or column with BLACK-RED-RED-BLACK should
     * be removed by the resizing algorithm. 
     */
    private PicGrabber basicTestPicture() {
        PicGrabber p = new PicGrabber(4, 4);
        p.setPixelColor(0, 0, Color.BLACK);
        p.setPixelColor(0, 1, Color.BLACK);
        p.setPixelColor(0, 2, Color.BLACK);
        p.setPixelColor(0, 3, Color.BLACK);
        p.setPixelColor(1, 0, Color.BLACK);
        p.setPixelColor(1, 1, Color.RED);
        p.setPixelColor(1, 2, Color.RED);
        p.setPixelColor(1, 3, Color.BLACK);
        p.setPixelColor(2, 0, Color.BLACK);
        p.setPixelColor(2, 1, Color.RED);
        p.setPixelColor(2, 2, Color.YELLOW);
        p.setPixelColor(2, 3, Color.BLACK);
        p.setPixelColor(3, 0, Color.BLACK);
        p.setPixelColor(3, 1, Color.BLACK);
        p.setPixelColor(3, 2, Color.BLACK);
        p.setPixelColor(3, 3, Color.BLACK);
        return p;
    }
    
    /**
     * Sets up a 4x4 picture whose pixels are:
     * (BLACK) (BLACK) (BLACK) (BLACK)
     * (BLACK) (YELLOW) (RED) (BLACK)
     * (BLACK) (RED) (RED) (BLACK)
     * (BLACK) (BLACK) (BLACK) (BLACK)
     * 
     * In this case, a row or column with BLACK-RED-RED-BLACK should
     * be removed by the resizing algorithm.
     */
    private PicGrabber basicTestPictureInverted() {
        PicGrabber p = new PicGrabber(4, 4);
        p.setPixelColor(0, 0, Color.BLACK);
        p.setPixelColor(0, 1, Color.BLACK);
        p.setPixelColor(0, 2, Color.BLACK);
        p.setPixelColor(0, 3, Color.BLACK);
        p.setPixelColor(1, 0, Color.BLACK);
        p.setPixelColor(1, 1, Color.YELLOW);
        p.setPixelColor(1, 2, Color.RED);
        p.setPixelColor(1, 3, Color.BLACK);
        p.setPixelColor(2, 0, Color.BLACK);
        p.setPixelColor(2, 1, Color.RED);
        p.setPixelColor(2, 2, Color.RED);
        p.setPixelColor(2, 3, Color.BLACK);
        p.setPixelColor(3, 0, Color.BLACK);
        p.setPixelColor(3, 1, Color.BLACK);
        p.setPixelColor(3, 2, Color.BLACK);
        p.setPixelColor(3, 3, Color.BLACK);
        return p;
    }

}
