import React from 'react';
import {Link} from "react-router-dom";
import logo from '../assets/Stockbird-Logo.png';
import othlogo from '../assets/othlogo.png';
import Typography from '@mui/material/Typography';

export default function Impressum() {
    return (
        <>
            <div>
              <div className="spHeader">
                <div className="logoSpace">
                  <Link to="/">
                    <img id="splogo" src={logo} alt="Stockbird Logo" />
                  </Link>
                </div>
                <div className="impressumSpace">
                  <Link to="/impressum" style={{ color: 'grey', textDecoration: 'none' }}>
                    <Typography variant="body1">Impressum</Typography>
                  </Link>
                </div>
              </div>
              <div className='impressumBody'>
                <Typography variant='h3'>Impressum</Typography>
                <Typography id='projectBy' variant='body1'>
                    Stockbird - a project by
                </Typography>
                <Typography variant='body2'>
                    Baran Baygin
                </Typography>
                <Typography variant='body2'>
                    Michael Ippisch
                </Typography>
                <Typography variant='body2'>
                    Rebecca Kietzer
                </Typography>
                <Typography variant='body2'>
                    Luca Käsmann
                </Typography>
                <Typography variant='body2'>
                    Carl Küschall
                </Typography>
                <Typography variant='body2'>
                    Jonathan Okorafor
                </Typography>
                <Typography variant='body2'>
                    Michael Zimmet
                </Typography>
                <Typography id='collabWith' variant='body1'>
                    in collaboration with
                </Typography>
                <img id="othlogo" src={othlogo} alt="OTH AW Logo" />
                <Typography variant='body2'>
                    Ostbayerische Technische Hochschule Amberg-Weiden
                </Typography>
                <Typography variant='body2'>
                    Kaiser-Wilhelm-Ring 23
                </Typography>
                <Typography variant='body2'>
                    92224 Amberg
                </Typography>
              </div>
            </div>
        </>
    )
}