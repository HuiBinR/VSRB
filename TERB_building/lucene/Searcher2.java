
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Date;
import java.lang.Math;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.cn.smart.SmartChineseAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.BooleanQuery;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;
import org.omg.PortableServer.ID_ASSIGNMENT_POLICY_ID;
import org.apache.lucene.search.similarities.BM25Similarity;


import com.google.common.base.Charsets;
import com.google.common.io.Files;

public class Searcher2 {
	
	  /** Simple command-line based search demo. */
	  public static void main(String[] args) throws Exception {
	    
		String usage =
	      "Usage:\t java org.apache.lucene.demo.SearchFiles [-index dir] [-field f] [-repeat n] [-queries file] "
	       + "[-query string] [-raw] [-paging hitsPerPage]\n\n";
		
	    if (args.length > 0 && ("-h".equals(args[0]) || "-help".equals(args[0]))) {
	      System.out.println(usage);
	      System.exit(0);
	    }

	    String index = "index";
	    String field = "contents";
	    String queries = null;
	    int repeat = 0;
	    boolean raw = false;
	    String queryString = null;
	    int hitsPerPage = 10;
	    
	    for(int i = 0;i < args.length;i++) {
	      if ("-index".equals(args[i])) {
	        index = args[i+1];
	        i++;
	      } else if ("-field".equals(args[i])) {
	        field = args[i+1];
	        i++;
	      } else if ("-queries".equals(args[i])) {
	        queries = args[i+1];
	        i++;
	      } else if ("-query".equals(args[i])) {
	        queryString = args[i+1];
	        i++;
	      } else if ("-repeat".equals(args[i])) {
	        repeat = Integer.parseInt(args[i+1]);
	        i++;
	      } else if ("-raw".equals(args[i])) {
	        raw = true;
	      } else if ("-paging".equals(args[i])) {
	        hitsPerPage = Integer.parseInt(args[i+1]);
	        if (hitsPerPage <= 0) {
	          System.err.println("There must be at least 1 hit per page.");
	          System.exit(1);
	        }
	        i++;
	      }
	    }
	    
	    IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(index)));
	    IndexSearcher searcher = new IndexSearcher(reader);
	    //Analyzer analyzer = new SmartChineseAnalyzer();
	    Analyzer analyzer = new StandardAnalyzer();
	    BufferedReader in = null;
	    if (queries != null) {
	      in = Files.newReader(new File(queries),Charsets.UTF_8);
	    } else {
	      in = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
	    }
	    QueryParser parser = new QueryParser(field, analyzer);
	    while (true) {
	      if (queries == null && queryString == null) {                        // prompt the user
	        System.out.println("Enter query: ");
	      }

	      String line = queryString != null ? queryString : in.readLine();

	      if (line == null || line.length() == -1) {
	        break;
	      }

	      line = line.trim();
	      if (line.length() == 0) {
	        break;
	      }
	      
	      Query query = parser.parse(line);
	      System.out.println("Searching for: " + query.toString(field));
	            
	      if (repeat > 0) {                           // repeat & time as benchmark
	        Date start = new Date();
	        for (int i = 0; i < repeat; i++) {
	          searcher.search(query, 100);
	        }
	        Date end = new Date();
	        System.out.println("Time: "+(end.getTime()-start.getTime())+"ms");
	      }

	      doPagingSearch(in, searcher, query, hitsPerPage, raw, queries == null && queryString == null);
	      //searchTopKResults(in, searcher, query, hitsPerPage, raw, queries == null && queryString == null);
	      if (queryString != null) {
	        break;
	      }
	    }
	    reader.close();
	  }
	  
	  public static void searchResult(String index, String queries, int hitPerPage, String selSoftDesp) throws Exception{
		  String usage =
			      "Usage:\t java org.apache.lucene.demo.SearchFiles [-index dir] [-field f] [-repeat n] [-queries file] "
			       + "[-query string] [-raw] [-paging hitsPerPage]\n\n";

			    boolean raw = false;
			    String field = "contents";
			    //String queryString = null;
			    //int hitsPerPage = 10;
			    
			    File file = new File(selSoftDesp);
			    
			    System.out.println("search similar software ...");			    
			    IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(index)));
			    IndexSearcher searcher = new IndexSearcher(reader);
			    //searcher.setSimilarity(new BM25Similarity());

				//Analyzer analyzer = new SmartChineseAnalyzer(); #for Chinese
			    Analyzer analyzer = new StandardAnalyzer();
			    QueryParser parser = new QueryParser(field, analyzer);

			    BufferedReader in = Files.newReader(new File(queries),Charsets.UTF_8);
			    
			    ArrayList<String> id_img = new ArrayList<>();
			    id_img = splitOfIdx(queries,"/");
			    String id_want = id_img.get(id_img.size()-1);
			    System.out.println(id_want);
			    
			    String line = null;
			    int rowCnt = 0;
			    while ((line=in.readLine())!=null) {
				  rowCnt++;
			      if (line == null || line.length() == -1) {
			        break;
			      }
			      line = line.trim();
			      if (line.length() == 0) {
			        continue;
			      }
			      if(line.contains("%")){
			    	  line = line.replace('%', ' ');
			      }
			      
				  line = line.replaceAll("OR", ""); 
			      line = line.replaceAll("AND", "");
			      line = line.replaceAll("NOT", ""); 

				  if(line.length() > 1000){
			    	  line=line.substring(0, 1000);
			      }
				 	
				  BooleanQuery.setMaxClauseCount(2048); 
			      boolean retry = true;
			      Query query = null;
			      while(retry){
			    	  try{
			    		  retry = false;
			    		  query = parser.parse(QueryParser.escape(line));
			    	  }catch(BooleanQuery.TooManyClauses e){
			    		  String defaultQueries = Integer.toString(BooleanQuery.getMaxClauseCount());
			    		  int oldQueries = Integer.parseInt(System.getProperty("org.apache.lucene.maxClauseCount", defaultQueries));
			    		  int newQuerise = oldQueries * 2;
			    		  System.setProperty("org.apache.lucene.maxClauseCount", Integer.toString(newQuerise));
			    		  BooleanQuery.setMaxClauseCount(newQuerise);
			    		  retry = true;
			    	  }
			    	 
			      }
			      if(rowCnt%100==0){
			    	  System.out.println(rowCnt + "done!");
			      }
			      //System.out.println("Searching for: " + query.toString(field));
		    	  searchTopKResults(in, searcher, query, hitPerPage, raw,  rowCnt, file, id_want);
			    }
			    reader.close();
	  }
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
      public static void searchTopKResults(BufferedReader in, IndexSearcher searcher, Query query,
    		  								int hitsPerPage, boolean raw, int sourceID, File file, String id_want) throws IOException{
		  //int allDocNums = 745908;
    	  TopDocs results = searcher.search(query, hitsPerPage);
    	  ScoreDoc[] hits = results.scoreDocs;
		  //System.out.println(hits.length);
		  
    	  
		  //double hitNum = Math.min(10, Math.floor(hits.length * hitsPerPage)); //hits number * selected percentage...
    	  int hitNum = Math.min(hitsPerPage, hits.length);
		  StringBuffer sb = new StringBuffer();
		  
//    	  sb.append(id + "#");
		  sb.append(id_want + "|");
    	  for(int i=0; i < hitNum; ++i){
	    	  if (raw) {                              // output raw format
		          System.out.println("doc="+hits[i].doc+" score="+hits[i].score);
		          continue;
		      }
	
		      Document doc = searcher.doc(hits[i].doc);
		      String path = doc.get("path");
		      if (path != null) {
		    	
		        String targetID = path.substring(path.lastIndexOf("/")+1);
				//sb.append(targetID + "-" + hits[i].score+"\t");
				sb.append(targetID + "|");


		      } else {
		          System.out.println((i+1) + ". " + "No path for this document");
		      }
    	  }
		  String tmpStr = sb.toString();
		  if(tmpStr.length() > 0){
		  	tmpStr = tmpStr.substring(0, tmpStr.length() - 1) + "|||\n";
		  }
	      Files.append(tmpStr, file, Charsets.UTF_8);
      }
	  /**
	   * This demonstrates a typical paging search scenario, where the search engine presents 
	   * pages of size n to the user. The user can then go to the next page if interested in
	   * the next hits.
	   * 
	   * When the query is executed for the first time, then only enough results are collected
	   * to fill 5 result pages. If the user wants to page beyond this limit, then the query
	   * is executed another time and all hits are collected.
	   * 
	   */
	  public static void doPagingSearch(BufferedReader in, IndexSearcher searcher, Query query, 
	                                     int hitsPerPage, boolean raw, boolean interactive) throws IOException {
	 
	    // Collect enough docs to show 5 pages
	    TopDocs results = searcher.search(query, 5 * hitsPerPage);
	    ScoreDoc[] hits = results.scoreDocs;
	    
	    int numTotalHits = results.totalHits;
	    System.out.println(numTotalHits + " total matching documents");

	    int start = 0;
	    int end = Math.min(numTotalHits, hitsPerPage);
	        
	    while (true) {
	      if (end > hits.length) {
	        System.out.println("Only results 1 - " + hits.length +" of " + numTotalHits + " total matching documents collected.");
	        System.out.println("Collect more (y/n) ?");
	        String line = in.readLine();
	        if (line.length() == 0 || line.charAt(0) == 'n') {
	          break;
	        }

	        hits = searcher.search(query, numTotalHits).scoreDocs;
	      }
	      
	      end = Math.min(hits.length, start + hitsPerPage);
	      
	      for (int i = start; i < end; i++) {
	        if (raw) {                              // output raw format
	          System.out.println("doc="+hits[i].doc+" score="+hits[i].score);
	          continue;
	        }

	        Document doc = searcher.doc(hits[i].doc);
	        String path = doc.get("path");
	        if (path != null) {
	          System.out.println((i+1) + ". " + path);
	          String title = doc.get("title");
	          if (title != null) {
	            System.out.println("   Title: " + doc.get("title"));
	          }
	        } else {
	          System.out.println((i+1) + ". " + "No path for this document");
	        }
	                  
	      }

	      if (!interactive || end == 0) {
	        break;
	      }

	      if (numTotalHits >= end) {
	        boolean quit = false;
	        while (true) {
	          System.out.print("Press ");
	          if (start - hitsPerPage >= 0) {
	            System.out.print("(p)revious page, ");  
	          }
	          if (start + hitsPerPage < numTotalHits) {
	            System.out.print("(n)ext page, ");
	          }
	          System.out.println("(q)uit or enter number to jump to a page.");
	          
	          String line = in.readLine();
	          if (line.length() == 0 || line.charAt(0)=='q') {
	            quit = true;
	            break;
	          }
	          if (line.charAt(0) == 'p') {
	            start = Math.max(0, start - hitsPerPage);
	            break;
	          } else if (line.charAt(0) == 'n') {
	            if (start + hitsPerPage < numTotalHits) {
	              start+=hitsPerPage;
	            }
	            break;
	          } else {
	            int page = Integer.parseInt(line);
	            if ((page - 1) * hitsPerPage < numTotalHits) {
	              start = (page - 1) * hitsPerPage;
	              break;
	            } else {
	              System.out.println("No such page");
	            }
	          }
	        }
	        if (quit) break;
	        end = Math.min(numTotalHits, start + hitsPerPage);
	      }
	    }
	  }
}
