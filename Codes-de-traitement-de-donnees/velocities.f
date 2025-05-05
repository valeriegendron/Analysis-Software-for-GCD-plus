      program velocities
*
      implicit double precision (a-h,m,o-z)
      parameter (nm=100000)

      character filename *5, filename2 *7, filename3 *13,
     +          filename4 *14

      dimension xs(nm), ys(nm), zs(nm), vxs(nm), vys(nm), vzs(nm),
     +          ms(nm)
      integer flagfd

      dimension U(nm), V(nm), W(nm), sqUW(nm), rad(nm)

* Read data for stars.

      write(6,1500)
 1500 format(/5x,'Enter dump number : ',$)
      read(5,*) ndump
      if(ndump.lt.10) then
           write(filename,1501) ndump
      else if(ndump.lt.100) then
           write(filename,1502) ndump
      else if(ndump.lt.1000) then
           write(filename,1503) ndump
      endif
 1501 format('s00',i1,'r')
 1502 format('s0',i2,'r')
 1503 format('s',i3,'r')
      open(unit=1,file=filename,status='old')

      ns=0
      do i=1,nm
           read(1,1000,end=99) xs(i), ys(i), zs(i), vxs(i), vys(i),
     +                         vzs(i), ms(i)
 1000      format(7(1pe13.5))
           ns=ns+1
      enddo
   99 close(unit=1)
      
* Calculate U, V, W, sqrt(U**2+W**2), and distance to z-axis.

      do i=1,ns
           rad(i)=sqrt(xs(i)**2+ys(i)**2)
           U(i)=(xs(i)*vxs(i)+ys(i)*vys(i))/rad(i)
           V(i)=(xs(i)*vys(i)-ys(i)*vxs(i))/rad(i)
           W(i)=vzs(i)
           sqUW(i)=sqrt(U(i)**2+W(i)**2)
      enddo

* Print results.

      filename2(1:5)=filename
      filename2(6:7)='_v'
      open(unit=2,file=filename2,status='unknown')

      do i=1,ns
           write(2,1001) xs(i), ys(i), zs(i), vxs(i), vys(i),
     +                   vzs(i), ms(i), U(i), V(i), W(i),
     +                   sqUW(i), rad(i)
 1001      format(12(1pe13.5))
      enddo
      close(unit=2)

!* Separate co- and counter-rotating stars.

!      nbco=0.
!      nbct=0.
!      nbfco=0.
!      nbfct=0.
!      filename3(1:10)=filename2
!      filename3(11:13)='_co'
!      open(unit=8,file=filename3,status='unknown')
!      filename3(11:13)='_ct'
!      open(unit=9,file=filename3,status='unknown')
!      open(unit=11,file='co_stars.dat',status='unknown')
!      open(unit=12,file='ct_stars.dat',status='unknown')
!      do i=1,ns
!           if(V(i).ge.0.) then 
!                write(8,1001) xs(i), ys(i), zs(i), vxs(i), vys(i),
!     +                        vzs(i), ms(i), ms0s(i), zHes(i), zCs(i),
!     +                        zNs(i), zOs(i), zNes(i), zMgs(i),
!     +                        zSis(i), zFes(i), zZs(i), zg_p(i), ts(i),
!     +                        id(i), flagfd(i), age(i), rhop(i), h(i),
!     +                        rhosp(i), up(i), rp(i), vph(i),
!     +                        vr(i), thetap(i), U(i), V(i), W(i),
!     +                        sqUW(i), rad(i)
!                write(11,1040) id(i)
! 1040           format(2x,i7)
!                nbco=nbco+1
!                if(V(i).ge.200.) nbfco=nbfco+1
!           else 
!                write(9,1001) xs(i), ys(i), zs(i), vxs(i), vys(i),
!     +                        vzs(i), ms(i), ms0s(i), zHes(i), zCs(i),
!     +                        zNs(i), zOs(i), zNes(i), zMgs(i),
!     +                        zSis(i), zFes(i), zZs(i), zg_p(i), ts(i),
!     +                        id(i), flagfd(i), age(i), rhop(i), h(i),
!     +                        rhosp(i), up(i), rp(i), vph(i),
!     +                        vr(i), thetap(i), U(i), V(i), W(i),
!     +                        sqUW(i), rad(i)
!                write(12,1040) id(i)
!                nbct=nbct+1
!                if(V(i).le.-200.) nbfct=nbfct+1
!           endif
!      enddo
!      close(unit=8)
!      close(unit=9)
!      close(unit=11)
!      close(unit=12)

!      write(6,2000) nbco, nbct
! 2000 format(/5x,'Number of co-rotating stars      : ',i7
!     +       /5x,'Number of counter-rotating stars : ',i7/)

!      write(6,2001) nbfco, nbfct
! 2001 format(/5x,'Number of fast co-rotating stars      : ',i7
!     +       /5x,'Number of fast counter-rotating stars : ',i7/)

      stop
      end

        
