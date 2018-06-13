import java.io.File;
public class Main {
	
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

		if(queryFile.exists() && queryFile.isDirectory()){
			
			File[] files = queryFile.listFiles();
			for(File file : files){
				String fileName = file.getPath();
				System.out.println(fileName);
				if(fileName.endsWith("mention1")){
					
					File resultFile = new File(candList + file.getName());
					if(resultFile.exists()){
						continue;
					}

					Searcher.searchResult(indexDir, fileName, hitPerPage, candList + "/" + file.getName());
				}
				else if(fileName.endsWith("mention2")){
					
					File resultFile = new File(candList + file.getName());
					if(resultFile.exists()){
						continue;
					}
					Searcher.searchResult(indexDir, fileName, hitPerPage, candList + "/" + file.getName());
				}
			}

		}

	}

}
