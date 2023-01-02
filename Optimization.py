from Parameters import *
from Cost_calculation import *

b=np.empty((2,Population_size))
label=os_sorted(os.listdir(f"{save_path}Processed_animals/"))
print(label)
for k in range(len(Img)):
    for j in range(times):
        b[1,times*k+j]=np.random.randint(len(os.listdir(f"{save_path}Processed_animals/{label[k]}/")))
        b[0,times*k+j]=k
b=b.astype('int64')

for k in range(len(Test_img)):
    gen=[]
    maxcost=[]
    bestimg=[]
    for l in range(len(Mutation_prob)):
        os.mkdir(f"{save_path}Results/{todaysDate}/Test_img_{k}_Mut_{Mutation_prob[l]}/")
        for i in range(Generations):
            b=Mutation(Roulette(b,k),Mutation_prob[l])
            cost=cost_calculation(choice,b,Test_img,k)[0]
            gen.append(i)
            fit=np.argmax(cost)
            bestimg.append(Img[b[0,fit]][:,:,b[1,fit]])
            maxcost.append(np.max(cost))
            fig, ax = plt.subplots(1,3)
            fig.set_size_inches(25, 5)
            ax[0].cla()
            ax[1].cla()
            ax[2].cla()
            ax[0].set_xlabel('generations')
            ax[0].set_ylabel('fitness')
            ax[0].scatter(gen, maxcost,s=0.5,color='royalblue')
            ax[0].plot(gen, maxcost,linewidth=1,color='royalblue')
            ax[1].set_xlabel('Population')
            ax[1].set_ylabel('Fitness')
            ax[1].scatter(np.arange(Population_size),cost,s=0.5,linewidth=0.5,color='royalblue')
            ax[1].plot(cost,linewidth=1,color='royalblue')
            ax[2].set_axis_off()
            ax[2].imshow(Test_img[k],cmap='gray')
            ax[2].set_title("Test_image")
            plt.close()
            fileName = f"{save_path}Results/{todaysDate}/Test_img_{k}_Mut_{Mutation_prob[l]}/{todaysDate}_GRAPH.pdf"
            title_text = f"Population : {Population_size}, CurrentGeneration : {i+1}/{Generations}, P(Crossing over) : {Cross_over_prob}, P(Mutation) : {Mutation_prob[l]}, Fitness function : {fun[choice]}  "
            print(i)
            fig.suptitle(title_text)
            if (i%10 == 0) | (i == Generations-1):
                fig.savefig(fileName,dpi=300,bbox_inches='tight', format='pdf')
                df = pd.DataFrame({"generations" : gen, "Fitness" : maxcost})
                df.to_csv(f"{save_path}Results/{todaysDate}/Test_img_{k}_Mut_{Mutation_prob[l]}/Fitness_vs_Generations_Mut_{Mutation_prob[l]}.csv",index=False)
                df2= pd.DataFrame({"Population" : list(range(1,Population_size+1)), "Fitness" : cost})
                df2.to_csv(f"{save_path}Results/{todaysDate}/Test_img_{k}_Mut_{Mutation_prob[l]}/Fitness_vs_Population_Gen_{i}_Mut_{Mutation_prob[l]}.csv",index=False)
        idxcost=np.empty((1,len(animaln)))
        print("The predicted class of the given animal is :")
        for i in range(len(animaln)):
            idx=np.where(b[0,:]==i)
            idxcost[0,i]=np.sum(b[1,idx])/np.sum(b[1,:])
        idx1=np.argsort(idxcost)
        idxcost=np.sort(idxcost)
        al1=[]
        al=[]
        for i in range(len(animaln)):
            al.append(animaln[idx1[0,i]])
            al1.append(100*idxcost[0,i])
            print(f"{animaln[idx1[0,i]]} : {100*idxcost[0,i]} %")
        df3=pd.DataFrame({"Animals":al,"Probability of prediction (%)" : al1})
        df3.to_csv(f"{save_path}Results/{todaysDate}/Test_img_{k}_Mut_{Mutation_prob[l]}/Prediction_MutationProb_Mut_{Mutation_prob[l]}.csv",index=False)
        plt.imshow(Test_img[k],cmap='gray')
        plt.axis("off")
        plt.savefig(f"{save_path}Results/{todaysDate}/Test_img_{k}_Mut_{Mutation_prob[l]}/Test_image.png",dpi=300,pad_inches=0,bbox_inches='tight')
        print(f"The most probable class is: {al[-1]}")