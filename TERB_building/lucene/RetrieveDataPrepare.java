
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;


public class RetrieveDataPrepare {
	/**
	 * 将wikipedia 图片caption文件，处理成每个caption对应一个文件。
	 * @param marketDesp
	 * @param outputDir
	 */
	public static void convertDesp2Files(String marketDesp, String outputDir) throws Exception{
		
		BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(marketDesp), "UTF-8"));
		String line = null;
		int row=0;
		while((line=reader.readLine())!=null){
			String desp = line;
			BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(outputDir+"/" +  row),"UTF-8")); 
			writer.write(desp+"\n");
			writer.close();	
			row++;
			if(row % 10000==0){
				System.out.println(row);
			}	
		}
		
		reader.close();
	}
	public static void main(String[] args) throws Exception{
		
		if(args.length!=2){
			System.out.println("Usage: java RetrieveDataPrepare [imageDesp] [outputDir]");
			System.exit(0);
		}
		String marketDesp = args[0];
		String outputDir = args[1];
		new File(outputDir).mkdirs();
		convertDesp2Files(marketDesp, outputDir);

	}

}
