#define LINUX

#include <linux/module.h>  /* Needed by all modules */
#include <linux/kernel.h>  /* Needed for KERN_ALERT */


int init_module(void)
{
  printk(KERN_ALERT "Hello world\n");
  return 0;
}


void cleanup_module(void)
{
  printk(KERN_ALERT "Goodbye world\n");
}  

MODULE_LICENSE("GPL");
