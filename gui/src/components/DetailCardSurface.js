import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import IconButton from '@material-ui/core/IconButton';
import PublishIcon from '@material-ui/icons/Publish';
import ContentLoader from 'react-content-loader'




const useStyles = makeStyles(theme=>({
  root: {
    margin: 'auto',
    width: 650,
    backgroundColor: theme.palette.primary.main,
  },
  media: {
    width:650,
    height: 650,
  },
  media2: {
    marginTop:20,
    width:650,
    height: 650,
  },
  titlebar:{
    
    height:80,
    width:'100%',
    background:
      'linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 70%, rgba(0,0,0,0) 100%)',
  },
  
}));



const News = () => (
  <ContentLoader
    viewBox="0 0 620 620"
    width={620}
    height={620}
    speed={2}
    backgroundColor="#fbfbfb"
    foregroundColor="#ecebeb"
  >
    <rect x="42.84" y="9.93" rx="5" ry="5" width="620" height="620" />
  </ContentLoader>
)

News.metadata = {
  name: 'Arthur Falcão',
  github: 'arthurfalcao',
  description: 'News List',
  filename: 'News',
}

export default function DetailCardSurface(props) {
  const classes = useStyles();
  const [file, setFile] = useState({imagePreviewUrl:'https://img.pngio.com/lungs-sketch-illustration-hand-drawn-animation-transparent-motion-animated-lung-png-1920_1080.png'})
  const [loading, setLoading] = useState(false)
  const [gotpred, setpred] = useState(false)
  const [selected, setselected] = useState(false)
  const [prediction, setprediction] = useState('Loading')
  
  

  const  sendXray = async () => {
    
    var formdata = new FormData();
    formdata.append("image", file.file, file.file.name);

    var requestOptions = {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
      },
      body: formdata,
      redirect: 'follow'
  };
  
  
  setLoading(true)
  await fetch("http://127.0.0.1:8000/api/xray-grad", requestOptions)
  .then(res => res.blob())
  .then(blob => {
      setLoading(false)
      setpred(true)
      console.log(blob)
      setFile({
        
        imagePreviewUrl:URL.createObjectURL(blob)
      })
    
  })
  .catch(error => console.log('error', error));
  
  fetch("http://127.0.0.1:8000/api/xray-pred", requestOptions)
  .then(res => res.text())
  .then(result => {
      console.log(result)
      setprediction(result)
    
  })
  .catch(error => console.log('error', error));
  
  }

  const handleImageChange = (e) => {
    let reader = new FileReader();
    let file = e.target.files[0];

    reader.onloadend = () => {
      setFile({
        file:file,
        imagePreviewUrl:reader.result
      })
    }
    setselected(true);
    reader.readAsDataURL(file)

  }

  return (
    <Card className={classes.root}>
      {
        !gotpred?
        <>
        <CardContent>
          <IconButton onClick={()=>{props.set(false); setpred(false)}}> <ArrowBackIcon/> </IconButton>
        </CardContent>
        {!loading?
        <CardMedia 
          className={classes.media}
          image={file.imagePreviewUrl}
          title="X-Ray"
        />
        :
        <div className={classes.media}>
          <News/>
        </div>
        }
        <CardActionArea>
        <CardContent>
          <div style={{display:'flex', justifyContent: 'space-between'}}>
            <div>
              <Typography color="inherit" gutterBottom variant="h5" component="h2">
                {props.disease}
              </Typography>
              {!loading?
              <Typography variant="body2" color="inherit" component="p">
              Upload the X-ray
              </Typography>
              :
              <Typography variant="body2" color="inherit" component="p">
              Getting your predictions, this may take a while. Please be patient!
              </Typography>
              }
            </div>
            <div>
              <IconButton onClick={()=>{document.getElementById('fileupload').click()}}><input id='fileupload' style={{display:'none'}} type="file" onChange={(e)=>handleImageChange(e)} /><PublishIcon/></IconButton>
            </div>
          </div>
        </CardContent>
      </CardActionArea>
      <CardActions>
      {!loading?
        <Button onClick={()=>{
          if(selected){
            sendXray()
          }
          else{
            alert("Please select a X-ray")
          }
          
          
          }} size="medium" color="secondary">
          Upload
        </Button>
      :
      <></>
      }
      </CardActions>
      </>
      :
      <>
      <CardContent>
        <IconButton onClick={()=>props.set(false)}> <ArrowBackIcon/> </IconButton>
      </CardContent>
      {!loading?
      <CardMedia 
        className={classes.media}
        image={file.imagePreviewUrl}
        title="X-Ray"
      />
      :
      <div>

      </div>
      }
      <CardActionArea>
      <CardContent>
        <div style={{display:'flex', justifyContent: 'space-between'}}>
          <div>
            <Typography color="inherit" gutterBottom variant="h5" component="h2">
              Prediction
            </Typography>
            <Typography variant="body2" color="inherit" component="p">
              {prediction}
            </Typography>
          </div>
        </div>
      </CardContent>
    </CardActionArea>
    </>
    }
    </Card>
  );
}
