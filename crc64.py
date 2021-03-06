# like zlib.crc32
# 使用两个辅助表（为了速度我们用了一个函数），  
# 之后删除该函数，因为我们再也用不着它了：  
CRCTableh = [0] * 256  
CRCTablel = [0] * 256  
def _inittables(CRCTableh, CRCTablel, POLY64REVh, BIT_TOGGLE):  
      for i in xrange(256):  
            partl = i 
            parth = 0L 
            for j in xrange(8):  
                  rflag = partl & 1L  
                  partl >>= 1L  
                  if parth & 1:  
                          partl ^= BIT_TOGGLE  
                  parth >>= 1L  
                  if rflag:  
                          parth ^= POLY64REVh  
            CRCTableh[i] = parth  
            CRCTablel[i] = partl  
# CRC64的高32位的生成多项式（低32位被假设为0）  
# 以及_inittables 所用的bit-toggle掩码   
POLY64REVh = 0xd8000000L 
BIT_TOGGLE = 1L << 31L 
# 运行函数来准备表  
_inittables(CRCTableh, CRCTablel, POLY64REVh, BIT_TOGGLE)  
# 删除我们不需要的名字，包括生成表的函数  
del _inittables, POLY64REVh, BIT_TOGGLE  
# 此模块公开了这两个函数：crc64和crc64digest  
# 碰撞:1/(2^64) -- http://zh.wikipedia.org/wiki/CRC32
def crc64(bytes, (crch, crcl)=(0,0)):  
      for byte in bytes:  
            shr = (crch & 0xFF) << 24 
            temp1h = crch >> 8L  
            temp1l = (crcl >> 8L) | shr  
            tableindex = (crcl ^ ord(byte)) & 0xFF  
            crch = temp1h ^ CRCTableh[tableindex]  
            crcl = temp1l ^ CRCTablel[tableindex]  
      return crch, crcl  
def crc64digest(aString):  
      return "%08X%08X" % (crc64(bytes))  
if _ _name_ _ == '_ _main_ _':  
        # 当此模块作为主脚本运行时，一个小测试/展示  
        assert crc64("IHATEMATH") == (3822890454, 2600578513)  
        assert crc64digest("IHATEMATH") == "E3DCADD69B01ADD1"  
        print 'crc64: dumb test successful' 
