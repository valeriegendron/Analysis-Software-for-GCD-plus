* Copied from program counter2.f, written by Simon Richard.
*
*     2019
*
      program detilt
      implicit double precision (a-h,m,o-z)

      parameter (nm=1000000)
      parameter (xunit=1)     ! length unit in kpc.
      parameter (vunit=1.0)   ! velocity unit in km/s.
      parameter (tunit=1.0)   ! time unit in Gyr.
      parameter (munit=1.0)  ! mass unit in M_sun.

      double precision jjx, jjy, jjz	
      double precision Js, Jxs, Jys, Jzs
      character filename *4, filename2 *5

      data filename2 /'****r'/
      
* For star.
      
      dimension xs(nm), ys(nm), zs(NM), vxs(NM), vys(NM), vzs(nm),
     +          ms(nm)

* For gas.
      
      dimension xg(nm), yg(nm), zg(nm), vxg(nm), vyg(nm), vzg(nm),
     +          mg(nm)
      
* For DM.
      
      dimension xd(Nm), yd(Nm), zd(Nm), vxd(Nm), vyd(Nm), vzd(Nm),
     +          md(Nm)

      write(6,1500)
 1500 format(/5x,'Enter dump number : ',$)
      read(5,*) ndump
      write(filename,1501) ndump
      if(ndump.lt.100) write(filename,1502) ndump
      if(ndump.lt.10) write(filename,1503) ndump
 1501 format('s',i3)
 1502 format('s0',i2)
 1503 format('s00',i1)
      open(unit=1,file=filename,status='old')
      filename2(1:4)=filename
      open(unit=11,file=filename2,status='unknown')

      filename(1:1)='g'
      open(unit=2,file=filename,status='old')
      filename2(1:4)=filename
      open(unit=12,file=filename2,status='unknown')

      filename(1:1)='d'
      open(unit=3,file=filename,status='old')
      filename2(1:4)=filename
      open(unit=13,file=filename2,status='unknown')

* Read data for stars.

      mstot=0.
      ns=0
      do i=1,nm
           read(1,153,end=80) xs(i), ys(i), zs(i), vxs(i), vys(i),
     +                        vzs(i), ms(i)
  153      format(7(1pe13.5))
           xs(i)=xs(i)*xunit
           ys(i)=ys(i)*xunit
           zs(i)=zs(i)*xunit
           vxs(i)=vxs(i)*vunit
           vys(i)=vys(i)*vunit
           vzs(i)=vzs(i)*vunit
           ms(i)=ms(i)*munit
           mstot=mstot+ms(i)
           ns=ns+1
      enddo
   80 close(unit=1)
 		 		
* Read data for gas.

      mgtot=0.
      ng=0
      do i=1,nm
           read(2,101,end=21) xg(i), yg(i), zg(i), vxg(i), vyg(i),
     +                        vzg(i), mg(i)
  101      format(7(1pe13.5))
           xg(i)=xg(i)*xunit
           yg(i)=yg(i)*xunit
           zg(i)=zg(i)*xunit
           vxg(i)=vxg(i)*vunit
           vyg(i)=vyg(i)*vunit
           vzg(i)=vzg(i)*vunit
           mg(i)=mg(i)*munit
           mgtot=mgtot+mg(i)
           ng=ng+1
      enddo
   21 close(unit=2)
      
* Read data for DM.

      mdtot=0.
      ndm=0
      do i=1,nm
           read(3,155,end=81) xd(i), yd(i), zd(i), vxd(i), vyd(i),
     +                        vzd(i), md(i)
  155      format(7(1pe13.5))
           xd(i)=xd(i)*xunit
           yd(i)=yd(i)*xunit
           zd(i)=zd(i)*xunit
           vxd(i)=vxd(i)*vunit
           vyd(i)=vyd(i)*vunit
           vzd(i)=vzd(i)*vunit
           md(i)=md(i)*munit
           mdtot=mdtot+md(i)
           ndm=ndm+1
      enddo
   81 close(unit=3)

      write(6,1000) ndm, ng, ns
 1000 format(/5x,'Number of dark matter particles : ',i6
     +       /5X,'Number of gas particles         : ',i6
     +       /5X,'Number of star particles        : ',i6)

      write(6,1010) mdtot, mgtot, mstot
 1010 format(/5x,'Total mass of dark matter : ',1pe13.6
     +       /5X,'Total mass of gas         : ',1pe13.6
     +       /5X,'Total mass of stars       : ',1pe13.6)

* Calculate center of mass of stars.
      
      xcm=0.0
      ycm=0.0
      zcm=0.0
      mt=0.0
      do i=1,ns
           xcm=xcm+xs(i)*ms(i)
           ycm=ycm+ys(i)*ms(i)
           zcm=zcm+zs(i)*ms(i)
           mt=mt+ms(i)
      enddo
      xcm=xcm/mstot
      ycm=ycm/mstot
      zcm=zcm/mstot

      write(6,1300) xcm, ycm, zcm
 1300 format(/5x,'Center of mass of stars : ',3(2x,1pe13.6))

* Shift origin to center of mass.

      do i=1,ns
           xs(i)=xs(i)-xcm
           ys(i)=ys(i)-ycm
           zs(i)=zs(i)-zcm
      enddo

      do i=1,ng
           xg(i)=xg(i)-xcm
           yg(i)=yg(i)-ycm
           zg(i)=zg(i)-zcm
      enddo

      do i=1,ndm
           xd(i)=xd(i)-xcm
           yd(i)=yd(i)-ycm
           zd(i)=zd(i)-zcm
      enddo	

* Calculate angular momentum of stars.

      Jxs=0.
      Jys=0.
      Jzs=0.
      Js=0.
      mts=0.
        
      do i=1,ns 
           mts=mts+ms(i)
           Jxs=Jxs+ms(i)*(ys(i)*vzs(i)-zs(i)*vys(i))
           Jys=Jys+ms(i)*(zs(i)*vxs(i)-xs(i)*vzs(i))
           Jzs=Jzs+ms(i)*(xs(i)*vys(i)-ys(i)*vxs(i))
      enddo
      Js=sqrt(Jxs*Jxs+Jys*Jys+Jzs*Jzs)

      if(Js.gt.0.) then
           jjx=Jxs/Js
           jjy=Jys/Js
           jjz=Jzs/Js
           costh=jjz
           sinth=sqrt(1.-jjz*jjz)
           if(sinth.gt.0.) then
                sinph=jjy/sinth
                cosph=jjx/sinth
           endif
      else 
           cosph=1.
           sinph=0.
      endif
        
      ax=costh*cosph
      bx=costh*sinph
      cx=-sinth
      ay=-sinph
      by=cosph
      cy=0.
      az=sinth*cosph
      bz=sinth*sinph
      cz=costh

      amx=ax*jjx+bx*jjy+cx*jjz
      amy=ay*jjx+by*jjy+cy*jjz
      amz=az*jjx+bz*jjy+cz*jjz

      write(6,2000) jjx, jjy, jjz
 2000 format(/5x,'Normalized angular momentum : ',3(2x,f10.8))
      write(6,2001) amx, amy, amz
 2001 format(/5x,'After rotation :              ',3(2x,f10.8))

* Rotate positions and velocities.

      do i=1,ns
           tx=xs(i)
           ty=ys(i)
           tz=zs(i)
           xs(i)=ax*tx+bx*ty+cx*tz
           ys(i)=ay*tx+by*ty+cy*tz
           zs(i)=az*tx+bz*ty+cz*tz

           tx=vxs(i)
           ty=vys(i)
           tz=vzs(i)
           vxs(i)=ax*tx+bx*ty+cx*tz
           vys(i)=ay*tx+by*ty+cy*tz
           vzs(i)=az*tx+bz*ty+cz*tz
      enddo

      do i=1,ng
           tx=xg(i)
           ty=yg(i)
           tz=zg(i)
           xg(i)=ax*tx+bx*ty+cx*tz
           yg(i)=ay*tx+by*ty+cy*tz
           zg(i)=az*tx+bz*ty+cz*tz
      
           tx=vxg(i)
           ty=vyg(i)
           tz=vzg(i)
           vxg(i)=ax*tx+bx*ty+cx*tz
           vyg(i)=ay*tx+by*ty+cy*tz
           vzg(i)=az*tx+bz*ty+cz*tz
      enddo

      do i=1,ndm
           tx=xd(i)
           ty=yd(i)
           tz=zd(i)
           xd(i)=ax*tx+bx*ty+cx*tz
           yd(i)=ay*tx+by*ty+cy*tz
           zd(i)=az*tx+bz*ty+cz*tz
      
           tx=vxd(i)
           ty=vyd(i)
           tz=vzd(i)
           vxd(i)=ax*tx+bx*ty+cx*tz
           vyd(i)=ay*tx+by*ty+cy*tz
           vzd(i)=az*tx+bz*ty+cz*tz
      enddo

* Print files.
      
      do i=1,ns
           write(11,153) xs(i), ys(i), zs(i), vxs(i), vys(i),
     +                   vzs(i), ms(i)
      enddo
			   
      do i=1,ng
           write(12,101) xg(i), yg(i), zg(i), vxg(i), vyg(i),
     +                   vzg(i), mg(i)
      enddo

      do i=1,ndm
           write(13,155) xd(i), yd(i), zd(i), vxd(i), vyd(i),
     +                   vzd(i), md(i)
      enddo

      close(unit=11)
      close(unit=12)
      close(unit=13)

      stop
      end
