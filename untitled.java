public String solution(int A, int B, int C, int D) {
        // write your code in Java SE 8
        //brutforce find all permutations and sort them.
        PriorityQueue <Integer> combination = new PriorityQueue<>(new Comparator<integer> () {
    		public int compare(Integer a, Integer b) {
       		return b - a;
    	}});

    	ArrayList<Integer> numList = Arrays.asList(A,B,C,D);
    	getPermutation(numList, 0, 0, combination);
    	if (combination.isEmpty())
    		return "Not Possible";
    	int maxTime = combination.poll();
    	System.out.println(maxTime);
    }

void getPermutation(ArrayList<Integer> a, int total, int index, PriorityQueue <Integer> combination)
    {
        // if size becomes 1 then prints the obtained
        // permutation
        if (index == a.size() && total/100 <= 23 && total % 100 <= 59)
        	combination.add(total);
       
        for (int i=index; i<size; i++)
        {
        	//swap the target to start of the array;
            Collections.swap(a,i,index);
            getPermutation(a,total * 10 + a[index],index + 1, combination);
            Collections.swap(a,i,index);

        }
    }