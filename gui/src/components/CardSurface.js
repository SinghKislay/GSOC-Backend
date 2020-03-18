import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles(theme=>({
  root: {
    margin: 'auto',
    width: '98%',
    backgroundColor: theme.palette.primary.main,
  },
  media: {
    height: 500,
    width:'100%',
    
  },
}));

export default function CardSurface(props) {
  const classes = useStyles();
  
  return (
    <Card className={classes.root}>
      
        <CardMedia
          className={classes.media}
          image="https://img.pngio.com/lungs-sketch-illustration-hand-drawn-animation-transparent-motion-animated-lung-png-1920_1080.png"
          title="X-Ray"
        />
        <CardActionArea>
        <CardContent onClick={()=>{props.set(true)}}>
          <Typography color="inherit" gutterBottom variant="h5" component="h2">
            {props.disease}
          </Typography>
          <Typography variant="body2" color="inherit" component="p">
          {props.para}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <Button size="small" color="secondary">
          Share
        </Button>
        <Button size="small" color="secondary">
          Learn More
        </Button>
      </CardActions>
    </Card>
  );
}
