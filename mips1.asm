.data
	a: .word 3
	b: .word 2
	c: .space 4
	d: .space 4
	e: .space 4
.text
	la $t0, a
	lw $s0, 0($t0)
	lw $s1, 4($t0)
	lw $t6, 4($t0)
	addi $t1, $zero, 1
Potencia: 
	beq $t6, $zero, FinBucle
	mul $t1, $t1, $s0,
	subi $t6, $t6, 1
	j Potencia
FinBucle: 
	sw $t1, 8($t0)
Suma: 
	add $t2, $s0, $s1
	add $t2, $t2, $t1
	sw $t2, 12($t0)
	addi $s2, $s2, 4
MulCuatro: 
	rem $t3, $t2, $s2
	subi $t2, $t2, 1
	bnez $t3, MulCuatro
	addi $t2, $t2, 1
	sw $t2, 16($t0)
	li $v0, 10
	syscall