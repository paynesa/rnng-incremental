# for variable in {1..10}
# do 
# 	./build/nt-parser/nt-parser-gen --dynet-mem 2000 -T training_oracle.txt -v unkified_mvrr.txt -f particle_processing/mvrr_30_$variable.txt --clusters clusters-train-berk.txt -m ntparse_gen_D0.3_2_256_256_16_256-pid20681.params --lstm_input_dim 256 --input_dim 256 --hidden_dim 256 --np 30


# done

for k in {1..10}
do 
	for x in {1..10}
	do
		echo $k-$x
	done
done