function labelList=getLabel()
    jointname=["nose","l-eye","r-eye","l-ear","r-ear","l-shoulder","r-shoulder","l-elbow","r-elbow","l-hand","r-hand","l-base","r-base","l-ankle","r-ankle","l-foot","r-foot"]

    labelList=[jointname+string("-x"),jointname+string("-y"),jointname+string("-z"),"x_R","y_R","theta_R","pan_R","t"]
end