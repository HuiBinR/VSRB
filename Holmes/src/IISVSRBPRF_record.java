import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.TreeSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.lang.Math;
import java.util.PriorityQueue;  
import java.util.Queue; 
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.RandomAccessFile;

public class IISVSRBPRF_record extends Thread {
	public HashMap<String, Set<String>> RELA2IDPAIRSET_MAP = new HashMap<String, Set<String>>();
	public HashMap<String, ArrayList<String>> TESTID2SIMIIDS_MAP = new HashMap<String, ArrayList<String>>();
	public HashMap<String, ArrayList<String>> RELA2PERFORMANCE4DIFFSIMISIZE_MAP = new HashMap<String, ArrayList<String>>();
	public HashMap<String, ArrayList<String>> CORRECTRELA2ANSWERRELA_MAP = new HashMap<String, ArrayList<String>>();
	public HashMap<String, Double> rela2weight = new HashMap<String, Double>();
	public final int total_giga_merge = 5272665; // 151841 5272665 938156
	
	public static void main(String[] args) throws Exception {
		IISVSRBPRF_record iis2eer = new IISVSRBPRF_record();
		iis2eer.run(args);
	}
	
	public void run(String[] args) {
		try {
			giga(args);			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	// lucene_size_n1n3: the size of the images searched for train and test
	// simi_img_size: the size of the images searched for the images that we get from the first step
	// top_prf = 1
	public void giga(String[] args) throws Exception {
		int lucene_size_n1n3 = Integer.parseInt(args[0]);
		int simi_img_size_n2 = Integer.parseInt(args[1]);
		int top_prf = Integer.parseInt(args[2]);
		String test_merge = "/data/xzdong/dingsiyuan/data/test/SubrelationMerge";
		String giga_merge = "/data/xzdong/dingsiyuan/data/train/Giga_merge";
		String result = "/data/xzdong/dingsiyuan/result/Giga_iisvsrb";
		String test_simi_img_list_path = "/data/xzdong/dingsiyuan/GigaVSRB_Result_top100";
		System.out.println("n1n3 = " + lucene_size_n1n3 + " , n2 = " + simi_img_size_n2);
		
		SystemUsingIISVSRB(giga_merge, test_merge, result, test_simi_img_list_path, lucene_size_n1n3, simi_img_size_n2, top_prf);
	}


	public void SystemUsingIISVSRB(String giga_merge, String test_merge, String result, String test_simi_img_list_path, int lucene_size, int simi_img_size, int top_prf) throws Exception {
		loadTestSimiImgList2Map(test_simi_img_list_path);
		loadRela2IDPairTreeset2HashMap(giga_merge, lucene_size);
		evaluate(test_merge, result, lucene_size, simi_img_size, top_prf);
		#printPerformance();
	}

	public void loadTestSimiImgList2Map(String test_simi_img_list_path) throws Exception {
		BufferedReader br = new BufferedReader(new FileReader(new File(test_simi_img_list_path)));
		String line = "";
		while ((line = br.readLine()) != null) {
			ArrayList<String> s = splitOfIdx(line, "|");
			if (s.size() != 101) {
				System.out.println(s.size() + "There is something wrong in img_id to simi_ids file!");
				continue;
			}
			String key_id = s.get(0);
			s.remove(0);
			if (!TESTID2SIMIIDS_MAP.containsKey(key_id)) {
				TESTID2SIMIIDS_MAP.put(key_id, s);
			}
		}
		br.close();
		System.out.println("Img_id to simi_id_list map size = " + TESTID2SIMIIDS_MAP.size());
	}

	public void loadRela2IDPairTreeset2HashMap(String VSRB_path, int lucene_size) throws Exception {
		System.out.println("==== Loading Connective to img id pair set 2 HashMap ... ====");
		ArrayList<String> relations = getFilenameList(VSRB_path);

		for (int i = 0; i < relations.size(); ++i) {
			String relation = relations.get(i);
			System.out.println("Loading Relation : " + relation);
			String rela_path = VSRB_path + File.separator + relation;
			relation = relation.replace(".txt#merge", "").trim();
			BufferedReader br = new BufferedReader(new FileReader(new File(rela_path)));
			String line = "";
			ArrayList<String> m1m2 = new ArrayList<String>();
			ArrayList<String> m1_img_ids = new ArrayList<String>();
			ArrayList<String> m2_img_ids = new ArrayList<String>();
			TreeSet<String> id_pair = new TreeSet<String>();
			long count = 0;
			while ((line = br.readLine()) != null) {
				if ((count++ % 10000) == 0) {
				 	System.out.println(count);
				}
				m1m2 = splitOfIdx(line, "|||");
				m1_img_ids = splitOfIdx(m1m2.get(0), "|");
				m2_img_ids = splitOfIdx(m1m2.get(1), "|");

				int lucene_size1 = lucene_size <= m1_img_ids.size() ? lucene_size : m1_img_ids.size();
				int lucene_size2 = lucene_size <= m2_img_ids.size() ? lucene_size : m2_img_ids.size();
				for (int m = 0; m < lucene_size1; ++m) {
					String m1_img_id = m1_img_ids.get(m);
					for (int n = 0; n < lucene_size2; ++n) {
						String m2_img_id = m2_img_ids.get(n);
						id_pair.add(m1_img_id + "|" + m2_img_id);
					}
				}
			}
			br.close();
			if (!RELA2IDPAIRSET_MAP.containsKey(relation)) {
				RELA2IDPAIRSET_MAP.put(relation, id_pair);
			}

			if (!rela2weight.containsKey(relation)) {
				rela2weight.put(relation, 1.0 * count / total_giga_merge);
			}
		}
		System.out.println("Rela2IDPairset2HashMap size : " + RELA2IDPAIRSET_MAP.size());
	}

	public void evaluate(String test_dir, String result_dir, int lucene_size, int simi_img_size, int top_prf) throws Exception {
		ArrayList<String> answer_relas = getFilenameList(test_dir);
		
		for (int idx = 0; idx < answer_relas.size(); ++idx) {
			String answer_rela = answer_relas.get(idx);
			String path = test_dir + File.separator + answer_rela;
			String result_path = result_dir + File.separator + answer_rela;
			answer_rela = answer_rela.replace(".txt#merge", "");
			
			FileWriter fw = null;
			File dir = new File("/data/xzdong/dingsiyuan/result_id_rel/"+lucene_size +"_" + simi_img_size+"_"+top_prf+"/");
			if (dir.exists()) {
				if (dir.isDirectory()) {
					System.out.println("dir exists");
				} else {
					System.out.println("the same name file exists, can not create dir");
				}
			} else {
				System.out.println("dir not exists, create it ...");
				dir.mkdir();
			}
			File f=new File(dir+"/"+answer_rela);
			
			ArrayList<String> m1m2 = new ArrayList<String>();
			ArrayList<String> m1_img_ids = new ArrayList<String>();
			ArrayList<String> m2_img_ids = new ArrayList<String>();			
			BufferedReader br = new BufferedReader(new FileReader(new File(path)));
		    BufferedWriter bw = new BufferedWriter(new FileWriter(new File(result_path)));
			String line = "";
			int line_idx = 0;
			System.out.println("--- Processing test file : " + answer_rela + " ---");

			int total_test_count = 0;
			while ((line = br.readLine()) != null) {
				total_test_count ++;
				HashMap<String, Integer> rel_cnt = new HashMap<String, Integer>();
				
				m1m2 = splitOfIdx(line, "|||");
				m1_img_ids = splitOfIdx(m1m2.get(0), "|");
				m2_img_ids = splitOfIdx(m1m2.get(1), "|");
				HashMap<String, Double> rela_result = new HashMap<String, Double>();
				int lucene_size1 = lucene_size <= m1_img_ids.size() ? lucene_size : m1_img_ids.size();
				int lucene_size2 = lucene_size <= m2_img_ids.size() ? lucene_size : m2_img_ids.size();
				for (int i = 0; i < lucene_size1; ++i) {
					String m1_img_id = m1_img_ids.get(i);
					ArrayList<String> simi_id_list1 = TESTID2SIMIIDS_MAP.get(m1_img_id);
					if (simi_id_list1 == null) {
						System.out.println("NULL ID = " + m1_img_id);
					}
					for (int j = 0; j < lucene_size2; ++j) {
						String m2_img_id = m2_img_ids.get(j);
						ArrayList<String> simi_id_list2 = TESTID2SIMIIDS_MAP.get(m2_img_id);
						for (int m = 0; m < simi_img_size; ++m) {
							String m1_simi_id = simi_id_list1.get(m);
							for (int n = 0; n < simi_img_size; ++n) {
								String m2_simi_id = simi_id_list2.get(n);
								String ret_rela = getConnFromVSRBUsingThisPair(m1_simi_id, m2_simi_id);
									
								if (!ret_rela.equals("NA")) 
									
									if (rel_cnt.containsKey(ret_rela)) {
										rel_cnt.put(ret_rela, (int) (rel_cnt.get(ret_rela) + 1.0));
									} else {
										rel_cnt.put(ret_rela, (int) 1);
									}
									
								}
							}
						}
					}
				}
				String final_rela = vote4FinalConn(rela_result, answer_rela, top_prf);
				
				
				if (rel_cnt == null || rel_cnt.size() == 0) {
					rel_cnt.put("Other", 1);
				}
				List<Entry<String, Integer>> conn_result_list = new ArrayList<Entry<String, Integer>>(rel_cnt.entrySet());
				Collections.sort(conn_result_list, new Comparator<Map.Entry<String, Integer>>() {
				    public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
				        return (int)(o2.getValue() - o1.getValue());
				    }
				});
				//System.out.println(conn_result_list.size());
				try {
					fw = new FileWriter(f, true);
				} 
				catch (IOException e) {
					e.printStackTrace();
				}
				PrintWriter pw = new PrintWriter(fw);

				for(int i = 0 ; i < conn_result_list.size() ; i++) {
					pw.print(total_test_count+" "+conn_result_list.get(i)+" ");
					pw.flush();
				}
				try {
					fw.flush();
					pw.close();
					fw.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
				
				
				
//				System.out.println("### This test file's " + (++ total_test_count) + " instance " + answer_rela + "\'s result is : " + final_rela + " ###");
				bw.write(final_rela + "\n");

				if (!CORRECTRELA2ANSWERRELA_MAP.containsKey(answer_rela)) {
					ArrayList<String> answer_rela_list = new ArrayList<String>(); 
					answer_rela_list.add(final_rela);
					CORRECTRELA2ANSWERRELA_MAP.put(answer_rela, answer_rela_list);
				} else {
					ArrayList<String> answer_rela_list = CORRECTRELA2ANSWERRELA_MAP.get(answer_rela); 
					answer_rela_list.add(final_rela);
					CORRECTRELA2ANSWERRELA_MAP.put(answer_rela, answer_rela_list);
				}
				
				try {
					fw = new FileWriter(f, true);
				} 
				catch (IOException e) {
					e.printStackTrace();
				}
				PrintWriter pw2 = new PrintWriter(fw);
				pw2.println();
				pw2.flush();
				try {
					fw.flush();
					pw2.close();
					fw.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			System.out.println("/data/xzdong/dingsiyuan/result_id_rel/"+answer_rela);
			
			bw.flush();
			bw.close();
			br.close();
		}
	}

	
	public String vote4FinalConn(HashMap<String, Double> rela_result, String answer_rela, int top_prf) {
		if (rela_result == null || rela_result.size() == 0) {
			return "OTHER";
		}
		List<Entry<String, Double>> conn_result_list = new ArrayList<Entry<String, Double>>(rela_result.entrySet());
		Collections.sort(conn_result_list, new Comparator<Map.Entry<String, Double>>() {
		    public int compare(Map.Entry<String, Double> o1, Map.Entry<String, Double> o2) {
		        return (int)(o2.getValue() - o1.getValue());
		    }
		});

		return conn_result_list.get(0).getKey();
	}
	public boolean isThisIDPairBelongs2ThisRela(String relation, String m1_img_id, String m2_img_id) {
		if (RELA2IDPAIRSET_MAP.containsKey(relation)) { 
			Set<String> tmp_set = RELA2IDPAIRSET_MAP.get(relation);
			if (tmp_set.contains(m1_img_id + "|" + m2_img_id) || tmp_set.contains(m2_img_id + "|" + m1_img_id)) {
				return true;
			}
		}
		return false;
	}

	public String getConnFromVSRBUsingThisPair(String m1_img_id, String m2_img_id) {
		for (Entry<String, Set<String>> entry : RELA2IDPAIRSET_MAP.entrySet()) {
			String connective = entry.getKey();
			Set<String> tmp_set = entry.getValue();
			if (tmp_set.contains(m1_img_id + "|" + m2_img_id) || tmp_set.contains(m2_img_id + "|" + m1_img_id)) {
				return connective;
			}
		}
		return "NA";
	}

	public ArrayList<String> splitOfIdx(String line, String reg) {
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

	public ArrayList<String> getFilenameList(String path) {
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

}

