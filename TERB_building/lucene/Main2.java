import java.awt.List;
import java.awt.image.SinglePixelPackedSampleModel;
import java.awt.print.Printable;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;
import java.util.Map.Entry;
import java.util.concurrent.ArrayBlockingQueue;
public class Main2 {
	
	public static ArrayList<String> splitOfIdx(String line, String reg) {
		int start = 0;
		int end = -1;
		int reg_len = reg.length();
		ArrayList<String> ss = new ArrayList<>();
		while ((end = line.indexOf(reg, start)) >=0) {
			if (!line.substring(start, end).equals("")) {
				ss.add(line.substring(start, end));
			}
			start = end + reg_len;
		}
		if (!line.substring(start).equals("")) {
			ss.add(line.substring(start));
		}
		return ss;
	}

	public static ArrayList<String> getFilenameList(String path) {
		ArrayList<String> foldername_list = new ArrayList<String>();
		File file = new File(path);
		File[] file_list = file.listFiles();
		for(File each_file : file_list) {
			if(!each_file.isDirectory()) {
				foldername_list.add(each_file.getName());
			}
		}
		return foldername_list;
	}

	
	public static void main(String[] args) throws Exception{
		
		if(args.length != 5){
			System.out.println("Usage: java Main [dataPath] [indexPath] [queryPath] [candList] [topN]");
			System.exit(0);
		}
		//image captions path
		String dataPath = args[0];
		//index path
		String indexDir = args[1];
		
		//mention file dir...
		String queryPath = args[2];
		//similar captions dir..
		String candList = args[3];
		
		int hitPerPage = Integer.parseInt(args[4]); //percentage of hited page

//Index.buildIndex(indexDir, dataPath);
		
		File queryFile = new File(queryPath);
		
		
		
		System.out.println("queryPath: " + queryPath);
		System.out.println("retrive result: " + candList);
		
//		VSRBResultop100 get
		Set<String> test_img_id = new HashSet<String>();
		
		if(queryFile.exists() && queryFile.isDirectory()){
			File[] files = queryFile.listFiles();
			for(File file : files){
				String fileName = file.getPath();
				System.out.println(fileName);
				BufferedReader br = new BufferedReader(new FileReader(new File(fileName)));

				ArrayList<String> m1m2 = new ArrayList<String>();
				ArrayList<String> m1_img_ids = new ArrayList<String>();
				ArrayList<String> m2_img_ids = new ArrayList<String>();	
				String line = "";
				int line_idx = 0;
				while ((line = br.readLine()) != null) {
					m1m2 = splitOfIdx(line, "|||");
					m1_img_ids = splitOfIdx(m1m2.get(0), "|");
					m2_img_ids = splitOfIdx(m1m2.get(1), "|");
					for(String m1: m1_img_ids) {
						test_img_id.add(m1);
					}
					for(String m2: m2_img_ids) {
						test_img_id.add(m2);
					}
					
				}
			}
		}
		
//		read file
		
		Set<String> fileNames = new HashSet<String>();
		for(String single_test_id : test_img_id){
			fileNames.add(dataPath+"/"+single_test_id);
		}
//		Set<String> fileNames = new HashSet<String>();
//		fileNames.add(dataPath+"/"+"3");
		
		//if(queryFile.exists() && queryFile.isDirectory()){
			
			// File[] files = queryFile.listFiles();
		for (String filepath:fileNames) {
			File file = new File(filepath);
			
			
			//for(File file : files){
				String fileName = file.getPath();
				System.out.println(fileName);
//				if(fileName.endsWith("mention1")){
					
//					File resultFile = new File(candList);
//					if(resultFile.exists()){
//						continue;
//					}

					Searcher2.searchResult(indexDir, fileName, hitPerPage, candList);
//				}
//				else if(fileName.endsWith("mention2")){
//					
//					File resultFile = new File(candList + file.getName());
//					if(resultFile.exists()){
//						continue;
//					}
//					Searcher.searchResult(indexDir, fileName, hitPerPage, candList + "/" + file.getName());
//				}
			}
		
	}

}
